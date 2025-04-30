document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const generateForm = document.getElementById('generateForm');
    const promptInput = document.getElementById('prompt');
    const outputDiv = document.getElementById('output');
    const modelButtons = document.querySelectorAll('.model-select');
    const topicSelect = document.getElementById('topicSelect');
    const modelDescription = document.getElementById('modelDescription');

    // Current model state
    let currentModel = 'transformer';

    // Model descriptions in Chinese
    const modelDescriptions = {
        transformer: 'GPT-2：强大的语言模型，生成连贯的文本',
        markov: '马尔可夫链：基于统计的文本生成模型'
    };

    // Handle model selection
    modelButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const model = this.dataset.model;
            
            try {
                const response = await fetch('/change_model', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ model_type: model })
                });

                if (response.ok) {
                    // Update UI
                    currentModel = model;
                    modelButtons.forEach(btn => {
                        btn.classList.remove('active');
                    });
                    this.classList.add('active');
                    modelDescription.textContent = modelDescriptions[model];
                }
            } catch (error) {
                console.error('模型切换错误:', error);
            }
        });
    });

    // Handle form submission
    generateForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const prompt = promptInput.value.trim();
        if (!prompt) {
            outputDiv.innerHTML = '<div class="alert alert-danger">请输入关键词或短语</div>';
            return;
        }

        // Show loading state
        outputDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p>生成中...</p></div>';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    model_type: currentModel,
                    topic: topicSelect.value
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Format the output
                let outputHtml = '<div class="generated-text">';
                if (data.generated_text.startsWith(prompt)) {
                    outputHtml += `<span class="prompt">${prompt}</span>`;
                    outputHtml += `<span class="generated">${data.generated_text.substring(prompt.length)}</span>`;
                } else {
                    outputHtml += `<span class="generated">${data.generated_text}</span>`;
                }
                outputHtml += '</div>';
                outputHtml += `<div class="mt-2"><small class="text-muted">使用模型: ${data.model_used}</small></div>`;
                outputHtml += '<button class="btn btn-sm btn-outline-secondary mt-2 copy-button">复制文本</button>';
                
                outputDiv.innerHTML = outputHtml;

                // Add copy functionality
                const copyButton = outputDiv.querySelector('.copy-button');
                copyButton.addEventListener('click', async () => {
                    try {
                        await navigator.clipboard.writeText(data.generated_text);
                        copyButton.textContent = '已复制！';
                        setTimeout(() => {
                            copyButton.textContent = '复制文本';
                        }, 2000);
                    } catch (err) {
                        console.error('复制失败:', err);
                        copyButton.textContent = '复制失败';
                    }
                });
            } else {
                outputDiv.innerHTML = `<div class="alert alert-danger">${data.error || '生成文本时发生错误'}</div>`;
            }
        } catch (error) {
            console.error('生成错误:', error);
            outputDiv.innerHTML = '<div class="alert alert-danger">生成文本时发生错误</div>';
        }
    });

    // Set initial model description
    modelDescription.textContent = modelDescriptions[currentModel];
});
