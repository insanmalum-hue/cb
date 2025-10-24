// Global variables
let sessionId = localStorage.getItem('chatbot_session_id');
let messageCount = 0;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const progressBar = document.getElementById('progressBar');
const statusText = document.getElementById('statusText');
const typingIndicator = document.getElementById('typingIndicator');

/**
 * Initialize the chat application
 */
async function init() {
    try {
        // Check if session exists
        if (!sessionId) {
            // Create new session
            const response = await fetch('/api/session/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();
            sessionId = data.session_id;

            // Save to localStorage
            localStorage.setItem('chatbot_session_id', sessionId);
            console.log('New session created:', sessionId);
        } else {
            console.log('Using existing session:', sessionId);
        }

        // Update status
        updateStatus('Ready to chat');

    } catch (error) {
        console.error('Initialization error:', error);
        updateStatus('Error initializing chat');
        addMessage('bot', 'Sorry, there was an error initializing the chat. Please refresh the page.');
    }
}

/**
 * Send user message to the server
 */
async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Disable input while processing
    messageInput.disabled = true;
    sendButton.disabled = true;

    // Add user message to chat
    addMessage('user', message);

    // Clear input
    messageInput.value = '';

    // Show typing indicator
    showTyping();

    try {
        // Send message to server
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        const data = await response.json();

        // Hide typing indicator
        hideTyping();

        if (response.ok) {
            // Check if response contains code
            const containsCode = data.response.includes('```python');

            if (containsCode) {
                addCodeMessage(data.response);
            } else {
                addMessage('bot', data.response);
            }

            // Update progress
            if (data.metadata) {
                messageCount = data.metadata.message_count;
                updateProgress(messageCount);

                // Update hint based on progress
                updateHint(data.metadata.remaining);
            }
        } else {
            addMessage('bot', 'Sorry, there was an error processing your message. Please try again.');
        }

    } catch (error) {
        console.error('Send message error:', error);
        hideTyping();
        addMessage('bot', 'Network error. Please check your connection and try again.');
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

/**
 * Add a message to the chat
 */
function addMessage(type, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    // Auto scroll to bottom
    scrollToBottom();
}

/**
 * Add a code message with syntax highlighting
 */
function addCodeMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Parse code blocks
    const codeBlockRegex = /```python\n([\s\S]*?)```/g;
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
        // Add text before code block
        if (match.index > lastIndex) {
            const textBefore = text.substring(lastIndex, match.index);
            const textNode = document.createTextNode(textBefore);
            contentDiv.appendChild(textNode);
        }

        // Add code block
        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.textContent = match[1].trim();
        pre.appendChild(code);
        contentDiv.appendChild(pre);

        lastIndex = codeBlockRegex.lastIndex;
    }

    // Add remaining text
    if (lastIndex < text.length) {
        const textAfter = text.substring(lastIndex);
        const textNode = document.createTextNode(textAfter);
        contentDiv.appendChild(textNode);
    }

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    // Auto scroll to bottom
    scrollToBottom();
}

/**
 * Update progress bar and status
 */
function updateProgress(count) {
    const percentage = (count / 36) * 100;
    progressBar.style.width = `${percentage}%`;
    statusText.textContent = `Message ${count}/36`;
}

/**
 * Update status text
 */
function updateStatus(status) {
    statusText.textContent = status;
}

/**
 * Update hint text based on remaining messages
 */
function updateHint(remaining) {
    const hintElement = document.querySelector('.input-hint');

    if (remaining === 0) {
        hintElement.textContent = 'Sequence complete! Type "show code" to receive your Python code.';
        hintElement.style.color = '#4CAF50';
        hintElement.style.fontWeight = 'bold';
    } else if (remaining <= 5) {
        hintElement.textContent = `Only ${remaining} messages remaining...`;
        hintElement.style.color = '#FF9800';
    } else {
        hintElement.textContent = 'Chat naturally to progress through the sequence...';
    }
}

/**
 * Show typing indicator
 */
function showTyping() {
    typingIndicator.classList.add('active');
    scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTyping() {
    typingIndicator.classList.remove('active');
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Handle Enter key press
 */
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize chat
    init();

    // Send button click
    sendButton.addEventListener('click', sendMessage);

    // Enter key press
    messageInput.addEventListener('keypress', handleKeyPress);

    // Focus on input
    messageInput.focus();
});
