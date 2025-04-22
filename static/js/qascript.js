document.addEventListener('DOMContentLoaded', function() {
            const chatMessages = document.getElementById('chat-messages');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');

            // 发送消息函数
            function sendMessage() {
                const message = userInput.value.trim();
                console.log("message",message)
                if (message === '') return;

                // 添加用户消息到聊天界面
                addMessage(message, 'user');
                userInput.value = '';

                // 显示"正在输入"指示器
                const typingIndicator = document.createElement('div');
                typingIndicator.className = 'typing-indicator';
                typingIndicator.textContent = '小助手正在思考...';
                chatMessages.appendChild(typingIndicator);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // 发送请求到后端
                fetch('/qa/smart_query/', {
                    method: 'POST',  // 使用POST请求
                    // 告诉服务器请求体的数据格式是 JSON，后端需要按 JSON 解析数据
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // Django需要CSRF token
                    },
                    //发送的是JSON格式 将请求数据转换为 JSON 字符串 并放入请求体
                    // JSON.stringify() 用于将 JavaScript 对象转换为 JSON 格式的字符串
                    body: JSON.stringify({ query: message })
                })
                    //它将服务器返回的响应（response）解析为 JSON 格式的数据。因为之前设置了请求数据是 JSON 格式，所以这里假设服务器返回的数据也是 JSON 格式的，
                    // 调用 response.json() 方法将其转换为 JavaScript 对象
                .then(response => response.json())
                    //这是第二个 then 回调函数，在成功解析 JSON 数据后执行。它接收上一步解析得到的 JSON 数据（data
                .then(data => {
                    // 移除"正在输入"指示器
                    chatMessages.removeChild(typingIndicator);

                    // 处理响应数据
                    let responseText = '';
                    if (data.polished) {
                        responseText = data.polished;
                        console.log("responseText",responseText)
                    } else if (data.answer) {
                        responseText = data.answer;
                        console.log("responseText",responseText)
                    } else if (data.data) {
                        // 如果有结构化数据，可以格式化显示
                        responseText = formatData(data.data);
                        console.log("responseText",responseText)
                    } else {
                        responseText = '抱歉，我没有找到相关信息。';
                    }

                    addMessage(responseText, 'bot');
                })
                .catch(error => {
                    console.error('Error:', error);
                    chatMessages.removeChild(typingIndicator);
                    addMessage('抱歉，请求处理时出现了问题。', 'bot');
                });
            }

            // 添加消息到聊天界面
            function addMessage(text, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                // messageDiv.innerHTML= text;
                messageDiv.innerHTML = text;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            // 格式化返回的数据
            function formatData(data) {
                if (!data || data.length === 0) {
                    return '<div class="no-result">没有找到相关结果。</div>';
                }

                let result = '<div class="attractions-container">';

                data.forEach((item, index) => {
                     // let desc = attraction.desc || '暂无描述';
                    console.log('item',item)

                    const period = item.d.period !== undefined && item.d.period !== null && item.d.period !=="nan"
    ? item.d.period
    : "未知";

                    result += `
                        <div class="attraction-card">
                            <div class="attraction-header">
                                <h3>${item.d.name || '未命名科室'}</h3>
                                <div class="rating">⭐ ${item.dept.name  || '无行业'}</div>
                            </div>
                            
                           
                   
         
                            <div class="attraction-desc">
                                  
                                 高发人群：${item.d.age}<br>
                                 
                                 检查项：${item.d.checklist}<br>
                                 治疗周期：${period}<br>
                                 治疗方法：${item.d.treatment}
                                   
                            </div>
                        </div>
                    `;
                });

                result += '</div>';
                return result;
            }

// 添加更多CSS样式
const css = `
<style>

    .attractions-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    .attraction-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 16px;
        background-color: white;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .attraction-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .attraction-header h3 {
        margin: 0;
        color: #333;
        font-size: 18px;
        font-weight: 600;
    }
    
    .rating {
        background-color: #4CAF50;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 14px;
        font-weight: bold;
        white-space: nowrap;
    }
    
    .image-container {
        margin-bottom: 12px;
        border-radius: 8px;
        overflow: hidden;
        max-height: 220px;
    }
    
    .attraction-image {
        width: 100%;
        height: auto;
        max-height: 220px;
        object-fit: cover;
        transition: transform 0.3s;
    }
    
    .attraction-image:hover {
        transform: scale(1.02);
    }
    
    .attraction-desc {
        color: #555;
        line-height: 1.7;
        font-size: 15px;
        text-align: justify;
    }
    
    .no-result {
        text-align: center;
        color: #888;
        padding: 20px;
        font-style: italic;
    }
    
    @media (max-width: 600px) {
        .attraction-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
        }
        
        .rating {
            align-self: flex-end;
        }
        
        .attraction-desc {
            font-size: 14px;
        }
    }
    .attraction-desc {
    font-family: Arial, sans-serif; /* 更改字体为 Arial，如果系统没有 Arial 字体，会使用 sans-serif 替代 */
    font-size: 16px; /* 增大字体大小为 16 像素 */
    font-weight: bold; /* 设置字体加粗 */
}
.attraction-desc::before {
    font-weight: bold;
    font-size: 18px; /* 标题字体稍大一点，更突出 */
    color: #333; /* 标题颜色设为深灰色，看起来更沉稳 */
    display: block; /* 让标题单独占一行 */
}
</style>
`;

// 将样式添加到head中
document.head.insertAdjacentHTML('beforeend', css);

            // 获取CSRF token的函数（Django需要）
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            // 事件监听
            sendButton.addEventListener('click', sendMessage);
            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        });