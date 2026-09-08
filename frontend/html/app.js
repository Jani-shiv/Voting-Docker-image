document.addEventListener('DOMContentLoaded', () => {
    const voterNameInput = document.getElementById('voter-name');
    const partyCards = document.querySelectorAll('.party-card');
    const voteBtn = document.getElementById('vote-btn');
    const statusMessage = document.getElementById('status-message');
    const resultsContainer = document.getElementById('results-container');

    let selectedParty = null;

    // Fetch initial results
    fetchResults();

    // Poll for live result updates every 5 seconds
    setInterval(fetchResults, 5000);

    // Handle party selection
    partyCards.forEach(card => {
        card.addEventListener('click', () => {
            partyCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            selectedParty = card.dataset.party;
            checkFormValidity();
        });
    });

    // Handle name input
    voterNameInput.addEventListener('input', checkFormValidity);

    function checkFormValidity() {
        if (voterNameInput.value.trim() !== '' && selectedParty !== null) {
            voteBtn.disabled = false;
        } else {
            voteBtn.disabled = true;
        }
    }

    // Handle voting
    voteBtn.addEventListener('click', async () => {
        const name = voterNameInput.value.trim();
        if (!name || !selectedParty) return;

        voteBtn.disabled = true;
        voteBtn.innerText = 'Casting vote...';

        try {
            const response = await fetch('/api/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: name, party: selectedParty })
            });

            const data = await response.json();

            if (response.ok) {
                showMessage(data.message, 'success');
                voterNameInput.value = '';
                partyCards.forEach(c => c.classList.remove('selected'));
                selectedParty = null;
                fetchResults();
            } else {
                showMessage(data.error || 'An error occurred', 'error');
            }
        } catch (error) {
            showMessage('Failed to connect to backend server', 'error');
        } finally {
            voteBtn.innerText = 'Cast Your Vote';
            checkFormValidity();
        }
    });

    function showMessage(msg, type) {
        statusMessage.textContent = msg;
        statusMessage.className = type === 'success' ? 'status-success' : 'status-error';
        statusMessage.classList.remove('hidden');

        setTimeout(() => {
            statusMessage.classList.add('hidden');
        }, 3000);
    }

    async function fetchResults() {
        try {
            const response = await fetch('/api/results');
            if (response.ok) {
                const results = await response.json();
                renderResults(results);
            }
        } catch (error) {
            console.error('Failed to fetch results', error);
        }
    }

    function renderResults(results) {
        resultsContainer.innerHTML = '';
        const sortedParties = Object.keys(results).sort((a, b) => results[b] - results[a]);

        sortedParties.forEach(party => {
            const count = results[party];
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `
                <span class="result-name">${party}</span>
                <span class="result-count">${count} Vote${count !== 1 ? 's' : ''}</span>
            `;
            resultsContainer.appendChild(div);
        });
    }
});
