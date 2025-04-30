document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const generateForm = document.getElementById('generateForm');
    const promptInput = document.getElementById('prompt');
    const outputDiv = document.getElementById('output');
    const modelButtons = document.querySelectorAll('.model-select');
    const topicSelect = document.getElementById('topicSelect');
    const modelDescription = document.getElementById('modelDescription');
    const errorMessages = document.getElementById('error-messages');

    // Current model state
    let currentModel = 'chatglm';
    let isGenerating = false;

    // Model descriptions in Chinese
    const modelDescriptions = {
        chatglm: 'ChatGLM：专为中文优化的大型语言模型，生成流畅自然的中文文本',
        qwen: '通义千问：阿里巴巴开发的中文大模型，理解力和生成能力强',
        transformer: 'GPT-2：强大的语言模型，生成连贯且富有创意的文本',
        markov: '马尔可夫链：基于统计的文本生成模型，适合短文本生成'
    };

    // Handle model selection
    modelButtons.forEach(button => {
        button.addEventListener('click', async function() {
            if (isGenerating) return; // Prevent model change during generation

            const model = this.dataset.model;
            this.classList.add('loading');

            try {
                const response = await fetch('/change_model', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ model_type: model })
                });

                const data = await response.json();

                if (response.ok) {
                    currentModel = model;
                    modelButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    modelDescription.textContent = modelDescriptions[model];

                    // Show success message
                    showNotification(data.message || '模型切换成功', 'success');
                } else {
                    throw new Error(data.error || '模型切换失败');
                }
            } catch (error) {
                showNotification(error.message, 'danger');
            } finally {
                this.classList.remove('loading');
            }
        });
    });

    // Show notification function
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show notification`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.querySelector('.container').insertAdjacentElement('afterbegin', notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Handle form submission
    generateForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (isGenerating) return;

        const prompt = promptInput.value.trim();
        if (!prompt) {
            showNotification(errorMessages.dataset.emptyPromptError, 'warning');
            return;
        }

        isGenerating = true;
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        // Show loading state with progress animation
        outputDiv.innerHTML = `
            <div class="generation-loading">
                <div class="progress mb-3">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"></div>
                </div>
                <p class="text-center">正在生成中，请稍候...</p>
            </div>
        `;

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
                // Format the output with enhanced styling
                let outputHtml = '<div class="generated-text">';
                if (data.generated_text.startsWith(prompt)) {
                    outputHtml += `<span class="prompt">${prompt}</span>`;
                    outputHtml += `<span class="generated">${data.generated_text.substring(prompt.length)}</span>`;
                } else {
                    outputHtml += `<span class="generated">${data.generated_text}</span>`;
                }
                outputHtml += '</div>';

                // Add metadata and controls
                outputHtml += `
                    <div class="generation-meta mt-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">使用模型: ${data.model_used}</small>
                            <button class="btn btn-sm btn-outline-primary copy-button">
                                <i class="bi bi-clipboard"></i> 复制文本
                            </button>
                        </div>
                    </div>
                `;

                outputDiv.innerHTML = outputHtml;

                // Add copy functionality
                const copyButton = outputDiv.querySelector('.copy-button');
                copyButton.addEventListener('click', async () => {
                    try {
                        await navigator.clipboard.writeText(data.generated_text);
                        copyButton.innerHTML = '<i class="bi bi-check2"></i> 已复制！';
                        setTimeout(() => {
                            copyButton.innerHTML = '<i class="bi bi-clipboard"></i> 复制文本';
                        }, 2000);
                    } catch (err) {
                        showNotification(errorMessages.dataset.copyError, 'danger');
                    }
                });
            } else {
                throw new Error(data.error || errorMessages.dataset.generationError);
            }
        } catch (error) {
            showNotification(error.message, 'danger');
            outputDiv.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
        } finally {
            isGenerating = false;
            submitButton.disabled = false;
        }
    });

    // Set initial model description and active state
    modelDescription.textContent = modelDescriptions[currentModel];
    modelButtons.forEach(btn => {
        if (btn.dataset.model === currentModel) {
            btn.classList.add('active');
        }
    });
});
