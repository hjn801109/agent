/**
 * 메인 앱 — 초기화 및 전역 상태 관리
 */

const App = (() => {
    let targetAgent = null;  // null이면 CEO 자동 분배 모드

    /**
     * 앱 초기화
     */
    async function init() {
        // 모듈 초기화
        Chat.init();

        // 데이터 로드
        await Promise.all([
            Agents.loadAgents(),
            Agents.loadSessions(),
            Agents.loadSharedMemory(),
            loadSettings(),
        ]);

        // AutoPilot 상태 체크
        checkAutopilotOnLoad();

        // 패널 탭 이벤트
        document.querySelectorAll('.panel-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                Agents.switchTab(tab.dataset.tab);

                // 세션/메모리 탭 클릭 시 새로고침
                if (tab.dataset.tab === 'sessions') Agents.loadSessions();
                if (tab.dataset.tab === 'memory') Agents.loadSharedMemory();
            });
        });

        // 힌트 카드 클릭
        document.querySelectorAll('.hint-card').forEach(card => {
            card.addEventListener('click', () => {
                const input = document.getElementById('chatInput');
                input.value = card.dataset.msg;
                input.focus();
            });
        });

        // CEO 모드 버튼
        document.getElementById('ceoModeBtn')?.addEventListener('click', () => {
            setTargetAgent(null);
        });
    }

    /**
     * 타겟 에이전트 설정 (null = CEO 자동 분배)
     */
    function setTargetAgent(agentId) {
        targetAgent = agentId;
        updateChatHeader();
    }

    function getTargetAgent() {
        return targetAgent;
    }

    /**
     * 채팅 헤더 업데이트
     */
    function updateChatHeader() {
        const badge = document.getElementById('targetBadge');
        const mode = document.getElementById('modeIndicator');

        if (targetAgent) {
            // 에이전트 직접 대화 모드
            const item = document.querySelector(`.agent-item[data-id="${targetAgent}"]`);
            const emoji = item?.querySelector('.agent-emoji')?.textContent || '';
            const name = item?.querySelector('.agent-name')?.textContent || targetAgent;
            badge.innerHTML = `${emoji} ${name}`;
            badge.style.display = 'inline-flex';
            mode.textContent = '직접 대화';
            mode.style.background = 'var(--bg-card)';
            mode.style.color = 'var(--rose-primary)';
        } else {
            badge.style.display = 'none';
            mode.textContent = '🧭 CEO 자동 분배';
            mode.style.background = 'var(--bg-tertiary)';
            mode.style.color = 'var(--text-muted)';
        }
    }

    /**
     * Ollama 설정 로드
     */
    async function loadSettings() {
        try {
            const resp = await fetch('/api/settings');
            const settings = await resp.json();

            // Ollama 상태 표시
            const dot = document.getElementById('ollamaStatus');
            dot.classList.toggle('online', settings.ollama_status);
            document.getElementById('ollamaStatusText').textContent =
                settings.ollama_status ? 'Ollama 연결됨' : 'Ollama 오프라인';

            // 모델 카드 렌더링
            renderModelCards(settings.available_models, settings.model);

            // Git 상태 표시
            if (settings.git) {
                updateGitStatus(settings.git);
            }
        } catch (err) {
            const dot = document.getElementById('ollamaStatus');
            dot.classList.remove('online');
            document.getElementById('ollamaStatusText').textContent = 'Ollama 연결 실패';
        }
    }

    /**
     * 모델 카드 렌더링
     */
    function renderModelCards(models, currentModel) {
        const list = document.getElementById('modelList');
        if (!list) return;

        list.innerHTML = models.map(m => {
            const isActive = m === currentModel;
            const shortName = m.replace(':latest', '');
            return `
                <div class="model-card ${isActive ? 'active' : ''}" data-model="${m}">
                    <span class="model-icon">🧠</span>
                    <span class="model-name">${shortName}</span>
                    <span class="model-check">✓</span>
                </div>
            `;
        }).join('');

        // 모델 없을 때
        if (models.length === 0) {
            list.innerHTML = '<div style="padding:8px;font-size:11px;color:var(--text-muted)">모델 없음</div>';
            return;
        }

        // 클릭 이벤트
        list.querySelectorAll('.model-card').forEach(card => {
            card.addEventListener('click', async () => {
                const model = card.dataset.model;

                // UI 즉시 업데이트
                list.querySelectorAll('.model-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');

                // 서버에 변경 요청
                await fetch('/api/settings', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model }),
                });
            });
        });
    }

    /**
     * Git 상태 UI 업데이트
     */
    function updateGitStatus(git) {
        const dot = document.getElementById('gitStatus');
        const text = document.getElementById('gitStatusText');

        if (!git.initialized) {
            dot.classList.remove('online');
            text.textContent = 'Git 미연결';
            return;
        }

        dot.classList.add('online');
        if (git.changed_files > 0) {
            text.textContent = `변경 ${git.changed_files}개`;
            dot.style.background = '#f39c12';
            dot.style.boxShadow = '0 0 8px rgba(243,156,18,0.4)';
        } else {
            text.textContent = 'GitHub 동기화됨';
            dot.style.background = '';
            dot.style.boxShadow = '';
        }
    }

    /**
     * 수동 GitHub 동기화
     */
    async function syncGithub() {
        const btn = document.getElementById('syncBtn');
        const text = document.getElementById('gitStatusText');

        btn.disabled = true;
        btn.textContent = '⏳ 동기화 중...';
        text.textContent = '동기화 진행 중...';

        try {
            const resp = await fetch('/api/sync/full', { method: 'POST' });
            const result = await resp.json();

            if (result.success) {
                text.textContent = '✅ 동기화 완료';
                // 새로고침
                Agents.loadSessions();
                Agents.loadSharedMemory();
            } else {
                text.textContent = '⚠️ 동기화 실패';
            }

            // 3초 후 상태 새로고침
            setTimeout(async () => {
                const resp2 = await fetch('/api/sync/status');
                const git = await resp2.json();
                updateGitStatus(git);
            }, 3000);
        } catch (err) {
            text.textContent = '⚠️ 동기화 오류';
        } finally {
            btn.disabled = false;
            btn.textContent = '🔄 동기화';
        }
    }
    /**
     * 모델 목록 새로고침 (새 모델 다운로드 후 사용)
     */
    async function refreshModels() {
        const list = document.getElementById('modelList');
        list.innerHTML = '<div style="padding:8px;font-size:11px;color:var(--text-muted)">🔄 새로고침 중...</div>';

        try {
            const resp = await fetch('/api/settings');
            const settings = await resp.json();
            renderModelCards(settings.available_models, settings.model);
        } catch (err) {
            list.innerHTML = '<div style="padding:8px;font-size:11px;color:var(--text-muted)">⚠️ 불러오기 실패</div>';
        }
    }

    // ── AutoPilot ──

    let _autopilotPolling = null;

    /**
     * 자율 업무 토글
     */
    async function toggleAutopilot() {
        const sw = document.getElementById('autopilotSwitch');
        const isOn = sw.checked;

        try {
            if (isOn) {
                const resp = await fetch('/api/autopilot/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ interval_minutes: 30 }),
                });
                const result = await resp.json();

                if (result.success) {
                    startAutopilotPolling();
                } else {
                    sw.checked = false;
                    alert(result.message);
                }
            } else {
                await fetch('/api/autopilot/stop', { method: 'POST' });
                stopAutopilotPolling();
                updateAutopilotUI({ running: false, status: 'off' });
            }
        } catch (err) {
            sw.checked = false;
            console.error('AutoPilot 토글 실패:', err);
        }
    }

    /**
     * 상태 폴링 시작 (15초 간격)
     */
    function startAutopilotPolling() {
        if (_autopilotPolling) return;
        pollAutopilotStatus();
        _autopilotPolling = setInterval(pollAutopilotStatus, 30000);
    }

    function stopAutopilotPolling() {
        if (_autopilotPolling) {
            clearInterval(_autopilotPolling);
            _autopilotPolling = null;
        }
    }

    async function pollAutopilotStatus() {
        try {
            const resp = await fetch('/api/autopilot/status');
            const data = await resp.json();
            updateAutopilotUI(data);

            // 꺼졌으면 폴링 중단
            if (!data.running) {
                stopAutopilotPolling();
                const sw = document.getElementById('autopilotSwitch');
                if (sw) sw.checked = false;
            }
        } catch (err) {
            // 연결 실패 시 무시
        }
    }

    /**
     * AutoPilot UI 업데이트
     */
    function updateAutopilotUI(data) {
        const bar = document.getElementById('autopilotBar');
        const icon = document.getElementById('autopilotIcon');
        const status = document.getElementById('autopilotStatus');
        const sw = document.getElementById('autopilotSwitch');

        if (!bar) return;

        if (data.running) {
            bar.classList.add('active');
            sw.checked = true;

            if (data.status === 'working') {
                icon.textContent = '⚡';
                status.textContent = `작업 중... (#${data.completed_cycles + 1})`;
            } else if (data.status === 'waiting' && data.next_run) {
                icon.textContent = '🌞';
                const next = new Date(data.next_run);
                const diff = Math.max(0, Math.floor((next - Date.now()) / 60000));
                status.textContent = `다음 작업 ${diff}분 후 (완료: ${data.completed_cycles}개)`;
            } else {
                icon.textContent = '🌞';
                status.textContent = `활성 (완료: ${data.completed_cycles}개)`;
            }
        } else {
            bar.classList.remove('active');
            icon.textContent = '🌙';
            status.textContent = data.completed_cycles > 0
                ? `비활성 (총 ${data.completed_cycles}개 완료)`
                : '비활성';
        }
    }

    /**
     * 초기화 시 autopilot 상태 체크
     */
    async function checkAutopilotOnLoad() {
        try {
            const resp = await fetch('/api/autopilot/status');
            const data = await resp.json();
            updateAutopilotUI(data);
            if (data.running) {
                document.getElementById('autopilotSwitch').checked = true;
                startAutopilotPolling();
            }
        } catch (err) {
            // 무시
        }
    }

    return { init, setTargetAgent, getTargetAgent, syncGithub, refreshModels, toggleAutopilot };
})();

// DOM 로드 후 초기화
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
