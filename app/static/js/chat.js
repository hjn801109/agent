/**
 * 채팅 모듈 — SSE 스트리밍 + 메시지 렌더링
 */

const Chat = (() => {
    let isStreaming = false;
    let currentAgentEl = null;   // 현재 스트리밍 중인 에이전트 메시지 요소
    let currentContent = '';     // 현재 스트리밍 중인 전체 내용

    const container = () => document.getElementById('chatContainer');
    const input = () => document.getElementById('chatInput');
    const sendBtn = () => document.getElementById('sendBtn');

    /**
     * 메시지 전송
     */
    async function send() {
        const msg = input().value.trim();
        if (!msg || isStreaming) return;

        // 사용자 메시지 렌더링
        renderUserMessage(msg);
        input().value = '';
        input().style.height = 'auto';

        // Welcome 화면 숨김
        const welcome = document.getElementById('welcomeScreen');
        if (welcome) welcome.remove();

        isStreaming = true;
        sendBtn().disabled = true;

        try {
            // SSE 스트리밍 요청
            const targetAgent = App.getTargetAgent();
            const body = JSON.stringify({
                message: msg,
                target_agent: targetAgent,
            });

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: body,
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop(); // 마지막 불완전한 라인 유지

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const raw = line.slice(6).trim();
                        if (raw === '[DONE]') continue;
                        try {
                            const event = JSON.parse(raw);
                            handleEvent(event);
                        } catch (e) {
                            // 파싱 실패 무시
                        }
                    }
                }
            }
        } catch (err) {
            renderSystemMessage(`⚠️ 오류: ${err.message}`);
        } finally {
            isStreaming = false;
            sendBtn().disabled = false;
            currentAgentEl = null;
            currentContent = '';
            // 작업 중 표시 해제
            document.querySelectorAll('.agent-item.working').forEach(el => {
                el.classList.remove('working');
            });
        }
    }

    /**
     * SSE 이벤트 처리
     */
    function handleEvent(event) {
        const { event: type, data } = event;

        switch (type) {
            case 'ceo_analyzing':
            case 'ceo_summarizing':
                renderSystemMessage(data.message);
                break;

            case 'ceo_distributed':
                renderDistribution(data);
                break;

            case 'web_searching':
                renderSystemMessage(`🔍 웹 검색 중: "${data.query}"...`);
                break;

            case 'search_done':
                if (data.count > 0) {
                    renderSystemMessage(`📋 검색 완료 — ${data.count}개 결과를 에이전트에게 전달합니다.`);
                } else {
                    renderSystemMessage('⚠️ 검색 결과가 없습니다. 기존 지식으로 진행합니다.');
                }
                break;

            case 'agent_start':
                startAgentMessage(data);
                break;

            case 'agent_chunk':
                appendChunk(data);
                break;

            case 'agent_done':
                finishAgentMessage(data);
                break;

            case 'workflow_done':
                renderSystemMessage('✅ 모든 작업이 완료되었습니다.');
                // 세션 목록 새로고침
                if (typeof Agents !== 'undefined') {
                    Agents.loadSessions();
                }
                break;

            case 'syncing':
                renderSystemMessage(data.message);
                break;

            case 'sync_done':
                if (data.success) {
                    renderSystemMessage('✅ GitHub 동기화 완료 — 세션 파일이 저장되었습니다.');
                } else {
                    renderSystemMessage('⚠️ GitHub 동기화 실패 — 로컬에는 저장되었습니다.');
                }
                break;

            case 'error':
                renderSystemMessage(`⚠️ ${data.message}`);
                break;
        }
    }

    /**
     * 사용자 메시지 렌더링
     */
    function renderUserMessage(text) {
        const el = document.createElement('div');
        el.className = 'message-user';
        el.textContent = text;
        container().appendChild(el);
        scrollToBottom();
    }

    /**
     * 시스템 메시지 렌더링
     */
    function renderSystemMessage(text) {
        const el = document.createElement('div');
        el.className = 'message-system';
        if (text.includes('분석') || text.includes('작성') || text.includes('...')) {
            el.innerHTML = `<div class="spinner"></div> ${text}`;
        } else {
            el.textContent = text;
        }
        container().appendChild(el);
        scrollToBottom();
    }

    /**
     * CEO 분배 결과 렌더링
     */
    function renderDistribution(data) {
        const el = document.createElement('div');
        el.className = 'distribution-card';

        let tasksHtml = data.tasks.map(t => `
            <div class="distribution-task">
                <span class="task-agent">${t.emoji} ${t.name}</span>
                <span class="task-desc">${t.task}</span>
            </div>
        `).join('');

        el.innerHTML = `
            <h3>🧭 CEO 작업 분배</h3>
            <p style="font-size:12px;color:var(--text-secondary);margin-bottom:10px">${data.summary}</p>
            ${tasksHtml}
        `;

        container().appendChild(el);
        scrollToBottom();
    }

    /**
     * 에이전트 메시지 시작
     */
    function startAgentMessage(data) {
        // 사이드바에 작업 중 표시
        const agentItem = document.querySelector(`.agent-item[data-id="${data.agent_id}"]`);
        if (agentItem) agentItem.classList.add('working');

        currentContent = '';

        const el = document.createElement('div');
        el.className = 'message-agent';
        el.id = `msg-${data.agent_id}-${Date.now()}`;

        el.innerHTML = `
            <div class="message-avatar" style="border-color: var(--agent-${data.agent_id})">${data.emoji}</div>
            <div class="message-body">
                <div class="message-header">
                    <span class="message-name" style="color: var(--agent-${data.agent_id})">${data.name}</span>
                    <span class="message-role">${data.task || ''}</span>
                </div>
                <div class="message-content"><span class="typing-cursor"></span></div>
            </div>
        `;

        container().appendChild(el);
        currentAgentEl = el;
        scrollToBottom();
    }

    /**
     * 스트리밍 청크 추가
     */
    function appendChunk(data) {
        if (!currentAgentEl) return;

        currentContent += data.content;
        const contentEl = currentAgentEl.querySelector('.message-content');
        if (contentEl) {
            contentEl.innerHTML = renderMarkdown(currentContent) + '<span class="typing-cursor"></span>';
            scrollToBottom();
        }
    }

    /**
     * 에이전트 메시지 완료
     */
    function finishAgentMessage(data) {
        if (currentAgentEl) {
            const contentEl = currentAgentEl.querySelector('.message-content');
            if (contentEl) {
                contentEl.innerHTML = renderMarkdown(currentContent);
            }
        }

        // 작업 중 표시 해제
        const agentItem = document.querySelector(`.agent-item[data-id="${data.agent_id}"]`);
        if (agentItem) agentItem.classList.remove('working');

        currentAgentEl = null;
        currentContent = '';
        scrollToBottom();
    }

    /**
     * 간단한 마크다운 렌더링
     */
    function renderMarkdown(text) {
        if (!text) return '';

        let html = text
            // 코드 블록
            .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
            // 인라인 코드
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            // 볼드
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            // 이탤릭
            .replace(/\*([^*]+)\*/g, '<em>$1</em>')
            // 헤딩
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            .replace(/^## (.+)$/gm, '<h2>$1</h2>')
            .replace(/^# (.+)$/gm, '<h1>$1</h1>')
            // 수평선
            .replace(/^---$/gm, '<hr>')
            // 테이블 (간단 처리)
            .replace(/^\|(.+)\|$/gm, (match) => {
                const cells = match.split('|').filter(c => c.trim());
                if (cells.every(c => /^[\s:-]+$/.test(c))) return ''; // separator
                const tag = 'td';
                return '<tr>' + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('') + '</tr>';
            })
            // 리스트
            .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
            .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
            // 줄바꿈
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');

        // li 태그 감싸기
        html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
        // tr 태그 감싸기
        html = html.replace(/(<tr>.*?<\/tr>)+/gs, '<table>$&</table>');

        return `<p>${html}</p>`;
    }

    /**
     * 스크롤 하단 이동
     */
    function scrollToBottom() {
        const c = container();
        requestAnimationFrame(() => {
            c.scrollTop = c.scrollHeight;
        });
    }

    /**
     * 초기화
     */
    function init() {
        // Enter 키로 전송
        input().addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                send();
            }
        });

        // textarea 자동 높이 조절
        input().addEventListener('input', () => {
            const el = input();
            el.style.height = 'auto';
            el.style.height = Math.min(el.scrollHeight, 120) + 'px';
        });

        // 전송 버튼
        sendBtn().addEventListener('click', send);
    }

    return { init, send, renderUserMessage, scrollToBottom };
})();
