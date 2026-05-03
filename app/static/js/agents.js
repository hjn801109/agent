/**
 * 에이전트 관리 모듈 — 에이전트 상세, 세션 히스토리
 */

const Agents = (() => {
    let agentList = [];
    let selectedAgent = null;

    /**
     * 에이전트 목록 로드
     */
    async function loadAgents() {
        try {
            const resp = await fetch('/api/agents');
            agentList = await resp.json();
            renderAgentList();
        } catch (err) {
            console.error('에이전트 로드 실패:', err);
        }
    }

    /**
     * 사이드바에 에이전트 목록 렌더링
     */
    function renderAgentList() {
        const el = document.getElementById('agentList');
        el.innerHTML = agentList.map(a => `
            <div class="agent-item" data-id="${a.id}" onclick="Agents.select('${a.id}')">
                <span class="agent-emoji">${a.emoji}</span>
                <div class="agent-info">
                    <div class="agent-name">${a.name}</div>
                    <div class="agent-title">${a.title}</div>
                </div>
            </div>
        `).join('');
    }

    /**
     * 에이전트 선택 → 상세 표시
     */
    async function select(agentId) {
        selectedAgent = agentId;

        // 활성 표시
        document.querySelectorAll('.agent-item').forEach(el => {
            el.classList.toggle('active', el.dataset.id === agentId);
        });

        // 상세 로드
        try {
            const resp = await fetch(`/api/agents/${agentId}`);
            const data = await resp.json();
            renderAgentDetail(data);

            // 우측 패널 탭 전환
            switchTab('agent');
        } catch (err) {
            console.error('에이전트 상세 로드 실패:', err);
        }

        // 채팅 헤더 업데이트
        App.setTargetAgent(agentId);
    }

    /**
     * 에이전트 상세 패널 렌더링
     */
    function renderAgentDetail(data) {
        const el = document.getElementById('agentDetail');
        el.innerHTML = `
            <div class="agent-detail-header">
                <div class="agent-detail-emoji">${data.emoji}</div>
                <div class="agent-detail-name" style="color:${data.color}">${data.name}</div>
                <div class="agent-detail-title">${data.title}</div>
            </div>

            <div class="detail-section">
                <div class="detail-section-title">
                    📝 페르소나
                    <button class="edit-btn" onclick="Agents.editField('${data.id}', 'prompt')">편집</button>
                </div>
                <div class="detail-section-content" id="field-prompt">${data.prompt || '(설정되지 않음)'}</div>
            </div>

            <div class="detail-section">
                <div class="detail-section-title">
                    🎯 목표
                    <button class="edit-btn" onclick="Agents.editField('${data.id}', 'goal')">편집</button>
                </div>
                <div class="detail-section-content" id="field-goal">${data.goal || '(설정되지 않음)'}</div>
            </div>

            <div class="detail-section">
                <div class="detail-section-title">
                    🧠 메모리
                </div>
                <div class="detail-section-content" id="field-memory">${data.memory || '(비어있음)'}</div>
            </div>
        `;
    }

    /**
     * 필드 편집 모드
     */
    function editField(agentId, field) {
        const contentEl = document.getElementById(`field-${field}`);
        const currentText = contentEl.textContent;
        if (currentText === '(설정되지 않음)' || currentText === '(비어있음)') {
            var text = '';
        } else {
            var text = currentText;
        }

        contentEl.outerHTML = `
            <textarea class="edit-textarea" id="edit-${field}">${text}</textarea>
            <div class="edit-actions">
                <button class="btn-sm btn-save" onclick="Agents.saveField('${agentId}', '${field}')">저장</button>
                <button class="btn-sm btn-cancel" onclick="Agents.select('${agentId}')">취소</button>
            </div>
        `;
    }

    /**
     * 필드 저장
     */
    async function saveField(agentId, field) {
        const textarea = document.getElementById(`edit-${field}`);
        const content = textarea.value;

        try {
            await fetch(`/api/agents/${agentId}/${field}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content }),
            });
            // 새로고침
            select(agentId);
        } catch (err) {
            alert('저장 실패: ' + err.message);
        }
    }

    /**
     * 세션 히스토리 로드
     */
    async function loadSessions() {
        try {
            const resp = await fetch('/api/sessions');
            const sessions = await resp.json();
            renderSessions(sessions);
        } catch (err) {
            console.error('세션 로드 실패:', err);
        }
    }

    /**
     * 세션 목록 렌더링
     */
    function renderSessions(sessions) {
        const el = document.getElementById('sessionList');
        if (!sessions.length) {
            el.innerHTML = '<p style="font-size:12px;color:var(--text-muted);text-align:center;padding:20px">아직 세션이 없습니다.</p>';
            return;
        }

        el.innerHTML = sessions.map(s => `
            <div class="session-item" onclick="Agents.viewSession('${s.id}')">
                <div class="session-date">📅 ${s.id}</div>
                <div class="session-command">${s.command || '(명령 없음)'}</div>
                <div class="session-files">
                    ${s.files.map(f => `<span class="session-file-badge">${f}</span>`).join('')}
                </div>
            </div>
        `).join('');
    }

    /**
     * 세션 상세 보기
     */
    async function viewSession(sessionId) {
        try {
            const resp = await fetch(`/api/sessions/${sessionId}`);
            const data = await resp.json();

            const el = document.getElementById('sessionList');
            let html = `
                <button class="btn-sm btn-cancel" onclick="Agents.loadSessions()" style="margin-bottom:12px">← 목록으로</button>
                <div class="session-date" style="font-size:14px;font-weight:600;margin-bottom:12px">📅 ${sessionId}</div>
            `;

            for (const [name, content] of Object.entries(data.files || {})) {
                html += `
                    <div class="detail-section">
                        <div class="detail-section-title">${name}</div>
                        <div class="detail-section-content">${content}</div>
                    </div>
                `;
            }

            el.innerHTML = html;
        } catch (err) {
            console.error('세션 로드 실패:', err);
        }
    }

    /**
     * 패널 탭 전환
     */
    function switchTab(tabId) {
        document.querySelectorAll('.panel-tab').forEach(t => {
            t.classList.toggle('active', t.dataset.tab === tabId);
        });
        document.getElementById('agentDetail').style.display = tabId === 'agent' ? 'block' : 'none';
        document.getElementById('sessionList').style.display = tabId === 'sessions' ? 'block' : 'none';
        document.getElementById('sharedMemory').style.display = tabId === 'memory' ? 'block' : 'none';
    }

    /**
     * 공유 메모리 로드
     */
    async function loadSharedMemory() {
        try {
            const resp = await fetch('/api/memory/shared');
            const data = await resp.json();
            renderSharedMemory(data);
        } catch (err) {
            console.error('공유 메모리 로드 실패:', err);
        }
    }

    /**
     * 공유 메모리 렌더링
     */
    function renderSharedMemory(data) {
        const el = document.getElementById('sharedMemory');
        el.innerHTML = `
            <div class="detail-section">
                <div class="detail-section-title">
                    🏢 회사 정체성
                    <button class="edit-btn" onclick="Agents.editShared('identity.md')">편집</button>
                </div>
                <div class="detail-section-content" id="shared-identity">${data.identity || '(비어있음)'}</div>
            </div>
            <div class="detail-section">
                <div class="detail-section-title">
                    🎯 공동 목표
                    <button class="edit-btn" onclick="Agents.editShared('goals.md')">편집</button>
                </div>
                <div class="detail-section-content" id="shared-goals">${data.goals || '(비어있음)'}</div>
            </div>
            <div class="detail-section">
                <div class="detail-section-title">
                    📌 의사결정 로그
                    <button class="edit-btn" onclick="Agents.editShared('decisions.md')">편집</button>
                </div>
                <div class="detail-section-content" id="shared-decisions">${data.decisions || '(비어있음)'}</div>
            </div>
        `;
    }

    /**
     * 공유 메모리 편집
     */
    function editShared(filename) {
        const key = filename.replace('.md', '');
        const contentEl = document.getElementById(`shared-${key}`);
        const text = contentEl.textContent === '(비어있음)' ? '' : contentEl.textContent;

        contentEl.outerHTML = `
            <textarea class="edit-textarea" id="edit-shared-${key}">${text}</textarea>
            <div class="edit-actions">
                <button class="btn-sm btn-save" onclick="Agents.saveShared('${filename}', '${key}')">저장</button>
                <button class="btn-sm btn-cancel" onclick="Agents.loadSharedMemory()">취소</button>
            </div>
        `;
    }

    /**
     * 공유 메모리 저장
     */
    async function saveShared(filename, key) {
        const textarea = document.getElementById(`edit-shared-${key}`);
        const content = textarea.value;

        try {
            await fetch(`/api/memory/shared/${filename}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content }),
            });
            loadSharedMemory();
        } catch (err) {
            alert('저장 실패: ' + err.message);
        }
    }

    return {
        loadAgents,
        select,
        editField,
        saveField,
        loadSessions,
        viewSession,
        switchTab,
        loadSharedMemory,
        editShared,
        saveShared,
    };
})();
