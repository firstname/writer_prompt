// 控制侧边栏模块的展开/收起
document.addEventListener('DOMContentLoaded', function() {
    const projectItems = document.querySelectorAll('.project-item h3');
    
    projectItems.forEach(item => {
        item.addEventListener('click', function() {
            const moduleList = this.nextElementSibling;
            moduleList.style.display = moduleList.style.display === 'none' ? 'block' : 'none';
        });
    });
});

// AJAX 表单提交处理
function submitForm(formId, successCallback) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (successCallback) {
                        successCallback(data);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
}

// 动态加载辅助内容
function loadHelperContent(url) {
    const helperPanel = document.querySelector('.helper-content');
    if (helperPanel) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                helperPanel.innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading helper content:', error);
            });
    }
}