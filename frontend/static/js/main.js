document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const methodSelect = document.getElementById('method-select');
    const langSelect = document.getElementById('lang-select');
    const expandCheck = document.getElementById('expand-check');
    const feedbackCheck = document.getElementById('feedback-check');
    
    const resultsContainer = document.getElementById('results-container');
    const resultsHeader = document.getElementById('results-header-text');
    const detectedBadge = document.getElementById('detected-badge');
    const detectedText = document.getElementById('detected-text');
    
    // Modal elements
    const docModal = document.getElementById('doc-modal');
    const modalClose = document.getElementById('modal-close');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    
    // Evaluation elements
    const runEvalBtn = document.getElementById('run-eval-btn');
    const evalResultsWrapper = document.getElementById('eval-results-wrapper');
    const evalTableBody = document.getElementById('eval-table-body');

    // Handle Search Form Submission
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        performSearch();
    });

    function performSearch() {
        const query = searchInput.value.trim();
        if (!query) return;

        const method = methodSelect.value;
        const targetLang = langSelect.value;
        const expand = expandCheck.checked;
        const feedback = feedbackCheck.checked;

        // Show loading state
        resultsHeader.textContent = 'Searching...';
        resultsContainer.innerHTML = '<div style="text-align: center; color: var(--text-secondary); width: 100%; padding: 2rem;">Retrieving documents from index...</div>';
        detectedBadge.className = 'detected-badge';
        
        const params = new URLSearchParams({
            q: query,
            method: method,
            target_lang: targetLang,
            expand: expand,
            feedback: feedback
        });

        fetch(`/search?${params.toString()}`)
            .then(res => res.json())
            .then(data => {
                renderResults(data);
            })
            .catch(err => {
                console.error(err);
                resultsHeader.textContent = 'Error';
                resultsContainer.innerHTML = `<div style="text-align: center; color: #EF4444; width: 100%; padding: 2rem;">An error occurred while searching: ${err.message}</div>`;
            });
    }

    function renderResults(data) {
        const results = data.results || [];
        
        // Show detected language
        if (data.query_detected) {
            detectedText.textContent = data.query_detected.toUpperCase();
            detectedBadge.className = `detected-badge ${data.query_detected}`;
        } else {
            detectedBadge.className = 'detected-badge';
        }

        resultsHeader.textContent = `Search Results (${results.length} found)`;
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div style="text-align: center; color: var(--text-secondary); width: 100%; padding: 3rem;">
                    No relevant documents found. Try adjusting options or translating your query.
                </div>`;
            return;
        }

        resultsContainer.innerHTML = '';
        results.forEach(doc => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.dataset.id = doc.doc_id;
            
            const scorePercent = Math.round(doc.score * 100);
            
            card.innerHTML = `
                <div class="result-header-row">
                    <h3 class="result-title">${doc.title}</h3>
                    <span class="lang-indicator ${doc.language}">${doc.language === 'english' ? '🇬🇧 English' : '🇪🇹 Amharic'}</span>
                </div>
                <p class="result-snippet">${doc.snippet}</p>
                <div class="result-footer">
                    <span class="score-badge">Relevance: ${scorePercent}%</span>
                    <span style="color: var(--text-muted);">Doc ID: ${doc.doc_id}</span>
                </div>
            `;

            // Open document modal on click
            card.addEventListener('click', () => {
                openDocModal(doc.doc_id);
            });

            resultsContainer.appendChild(card);
        });
    }

    // Modal Control
    function openDocModal(docId) {
        modalTitle.textContent = 'Loading Document...';
        modalBody.textContent = '';
        docModal.classList.add('active');

        fetch(`/document/${docId}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    modalTitle.textContent = 'Error';
                    modalBody.textContent = data.error;
                } else {
                    modalTitle.textContent = data.title;
                    modalBody.textContent = data.content;
                }
            })
            .catch(err => {
                modalTitle.textContent = 'Error';
                modalBody.textContent = `Could not retrieve document: ${err.message}`;
            });
    }

    modalClose.addEventListener('click', () => {
        docModal.classList.remove('active');
    });

    // Close modal on click outside content
    docModal.addEventListener('click', (e) => {
        if (e.target === docModal) {
            docModal.classList.remove('active');
        }
    });

    // Run Evaluation Trigger
    runEvalBtn.addEventListener('click', () => {
        runEvalBtn.textContent = 'Running Evaluation...';
        runEvalBtn.disabled = true;

        fetch('/evaluate', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    renderEvaluation(data.summary);
                } else {
                    alert(`Evaluation failed: ${data.error}`);
                }
            })
            .catch(err => {
                alert(`Error running evaluation: ${err.message}`);
            })
            .finally(() => {
                runEvalBtn.textContent = 'Execute Evaluation Run';
                runEvalBtn.disabled = false;
            });
    });

    function renderEvaluation(summary) {
        evalTableBody.innerHTML = '';
        evalResultsWrapper.style.display = 'block';

        for (const [configName, metrics] of Object.entries(summary)) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="font-weight: 500;">${configName}</td>
                <td>${(metrics.precision * 100).toFixed(1)}%</td>
                <td>${(metrics.recall * 100).toFixed(1)}%</td>
                <td>${(metrics.p_at_1 ? metrics.p_at_1 * 100 : metrics['p@1'] * 100).toFixed(1)}%</td>
                <td>${(metrics.p_at_3 ? metrics.p_at_3 * 100 : metrics['p@3'] * 100).toFixed(1)}%</td>
                <td>${(metrics.p_at_5 ? metrics.p_at_5 * 100 : metrics['p@5'] * 100).toFixed(1)}%</td>
                <td style="font-weight: 600; color: #C084FC;">${metrics.map.toFixed(3)}</td>
            `;
            evalTableBody.appendChild(tr);
        }
        
        // Scroll to evaluation panel
        document.getElementById('evaluation').scrollIntoView({ behavior: 'smooth' });
    }
});
