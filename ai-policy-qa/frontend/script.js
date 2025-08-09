// frontend/script.js
document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.getElementById('submit-button');
    const questionInput = document.getElementById('question-input');
    const responseArea = document.getElementById('response-area');
    const answerText = document.getElementById('answer-text');
    const sourcesContainer = document.getElementById('sources-container');
    const loadingSpinner = document.getElementById('loading-spinner');

    const API_URL = 'https://rag-teol.onrender.com/ask';

    const askQuestion = async () => {
        const question = questionInput.value.trim();
        if (!question) {
            alert('Please enter a question.');
            return;
        }

        // Show spinner and hide previous response
        loadingSpinner.classList.remove('hidden');
        responseArea.classList.add('hidden');
        submitButton.disabled = true;

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayResponse(data);

        } catch (error) {
            console.error('Error fetching data:', error);
            answerText.textContent = `Failed to get an answer. Error: ${error.message}`;
            sourcesContainer.innerHTML = '';
            responseArea.classList.remove('hidden');
        } finally {
            // Hide spinner and re-enable button
            loadingSpinner.classList.add('hidden');
            submitButton.disabled = false;
        }
    };

    const displayResponse = (data) => {
        // Display answer
        answerText.textContent = data.answer || 'No answer provided.';

        // Display sources
        sourcesContainer.innerHTML = ''; // Clear previous sources
        if (data.source_documents && data.source_documents.length > 0) {
            data.source_documents.forEach(doc => {
                const sourceDiv = document.createElement('div');
                sourceDiv.className = 'source-document';

                const metadata = doc.metadata || {};
                const pageNumber = metadata.page !== undefined ? `Page ${metadata.page + 1}` : 'Unknown Page';
                
                sourceDiv.innerHTML = `<strong>Source: ${pageNumber}</strong><p>${doc.content}</p>`;
                sourcesContainer.appendChild(sourceDiv);
            });
        } else {
            sourcesContainer.innerHTML = '<p>No source documents found.</p>';
        }

        responseArea.classList.remove('hidden');
    };

    submitButton.addEventListener('click', askQuestion);
    
    // Optional: Allow pressing Enter to submit
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
        }
    });
});