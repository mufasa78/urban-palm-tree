document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const form = document.getElementById('generation-form');
    const promptInput = document.getElementById('prompt');
    const generateBtn = document.getElementById('generate-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const resultDiv = document.getElementById('result');
    const errorMessageDiv = document.getElementById('error-message');
    const copyBtn = document.getElementById('copy-btn');
    
    // Function to handle the form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get the prompt value
        const prompt = promptInput.value.trim();
        
        // Validate the prompt
        if (!prompt) {
            showError('Please enter a keyword or phrase.');
            return;
        }
        
        // Reset previous results and errors
        resetOutput();
        
        // Show loading state
        setLoadingState(true);
        
        try {
            // Make API request to generate text
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });
            
            // Check if the response is OK
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to generate text');
            }
            
            // Parse the response data
            const data = await response.json();
            
            // Display the generated text
            displayGeneratedText(data.generated_text);
            
            // Enable the copy button
            copyBtn.disabled = false;
            
        } catch (error) {
            // Display error message
            showError(error.message || 'An error occurred while generating text.');
            console.error('Text generation error:', error);
        } finally {
            // Hide loading state
            setLoadingState(false);
        }
    });
    
    // Function to display the generated text
    function displayGeneratedText(text) {
        resultDiv.innerHTML = '';
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        resultDiv.appendChild(paragraph);
    }
    
    // Function to show error message
    function showError(message) {
        errorMessageDiv.textContent = message;
        errorMessageDiv.classList.remove('d-none');
    }
    
    // Function to reset the output area
    function resetOutput() {
        resultDiv.innerHTML = '<p class="text-muted">Generated text will appear here...</p>';
        errorMessageDiv.classList.add('d-none');
        errorMessageDiv.textContent = '';
        copyBtn.disabled = true;
    }
    
    // Function to set loading state
    function setLoadingState(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            loadingSpinner.classList.remove('d-none');
            resultDiv.classList.add('loading');
        } else {
            generateBtn.disabled = false;
            loadingSpinner.classList.add('d-none');
            resultDiv.classList.remove('loading');
        }
    }
    
    // Copy button functionality
    copyBtn.addEventListener('click', function() {
        const textToCopy = resultDiv.textContent;
        
        // Use the Clipboard API to copy text
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                // Change button text temporarily to indicate success
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="bi bi-check"></i> Copied!';
                copyBtn.classList.add('btn-success');
                copyBtn.classList.remove('btn-outline-secondary');
                
                // Restore original button text after a delay
                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                    copyBtn.classList.remove('btn-success');
                    copyBtn.classList.add('btn-outline-secondary');
                }, 2000);
            })
            .catch(err => {
                console.error('Could not copy text:', err);
                showError('Failed to copy text to clipboard');
            });
    });
    
    // Add example prompts for user guidance
    const examplePrompts = [
        "The future of technology",
        "Once upon a time",
        "Climate change is",
        "Artificial intelligence will",
        "The most important invention"
    ];
    
    // Randomly select an example for the placeholder
    promptInput.placeholder = examplePrompts[Math.floor(Math.random() * examplePrompts.length)];
});
