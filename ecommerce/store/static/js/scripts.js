document.addEventListener("DOMContentLoaded", function() {
    // Watch showcase logic
    const watchItems = document.querySelectorAll('.watch-item');
    let currentIndex = 0;  // Start from the first watch

    // Function to show the next watch
    function showNextWatch() {
        // Hide all watches
        watchItems.forEach((item) => {
            item.style.display = 'none';
        });

        // Show the current watch
        watchItems[currentIndex].style.display = 'block';

        // Increment the index to show the next watch
        currentIndex = (currentIndex + 1) % watchItems.length;  // Loop back to first if we reach the last watch
    }

    // Initially show the first watch
    showNextWatch();

    // Change the watch every 3 seconds (3000ms)
    setInterval(showNextWatch, 3000);

    // Chatbot toggle functionality
    const chatbotToggle = document.getElementById("chatbot-toggle");
    const chatbotBody = document.getElementById("chatbot-body");

    chatbotToggle.addEventListener("click", function() {
        chatbotBody.style.display = (chatbotBody.style.display === "none" || chatbotBody.style.display === "") ? "block" : "none";
    });

    // Send message functionality
    const chatbotSendButton = document.getElementById("chatbot-send");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotMessages = document.getElementById("chatbot-messages");

    chatbotSendButton.addEventListener("click", function() {
        const message = chatbotInput.value.trim();
        if (message) {
            const userMessage = document.createElement("div");
            userMessage.textContent = "You: " + message;
            chatbotMessages.appendChild(userMessage);
            chatbotInput.value = "";  // Clear the input field
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;  // Scroll to the bottom
        }
    });

    // Show images when they come into view
    window.addEventListener('scroll', function() {
        const images = document.querySelectorAll('.product-image');
        
        images.forEach(image => {
            if (image.getBoundingClientRect().top < window.innerHeight) {
                image.style.opacity = 1;  // Fade in when image is visible
            }
        });
    });

    // Send message to the backend and handle response
    function sendMessageToChatbot(message) {
        fetch("/chatbot-response/", {  // Make sure the URL matches the one in urls.py
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                displayMessage(data.response, "bot");
            }
        })
        .catch(error => console.error("Error:", error));
    }

    // Display messages in chatbot interface
    function displayMessage(message, sender) {
        const messageElement = document.createElement("p");
        messageElement.textContent = message;
        messageElement.className = sender === "user" ? "user-message" : "bot-message";
        document.getElementById("chatbot-messages").appendChild(messageElement);
        document.getElementById("chatbot-messages").scrollTop = document.getElementById("chatbot-messages").scrollHeight;
    }

    // CSRF token utility
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Send message on Enter key
    document.getElementById("chatbot-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            document.getElementById("chatbot-send").click();
        }
    });
});
