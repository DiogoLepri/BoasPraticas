document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message) => {
      setTimeout(() => {
        message.style.transition = 'opacity 0.5s ease';
        message.style.opacity = '0';
        setTimeout(() => {
          message.remove();
        }, 500);
      }, 5000);
    });
  
    const header = document.querySelector('.header');
    if (header) {
      const gradients = [
        'linear-gradient(135deg, #3498db, #2980b9)',
        'linear-gradient(135deg, #2980b9, #3498db)',
        'linear-gradient(135deg, #2c3e50, #3498db)',
        'linear-gradient(135deg, #3498db, #2c3e50)',
        'linear-gradient(135deg, #ff00a8, #ff5500)',
        'linear-gradient(135deg, #00ffc3, #00b3ff)'
      ];
      let currentIndex = 0;
      header.style.transition = 'background 1.5s ease';
      setInterval(() => {
        header.style.background = gradients[currentIndex];
        currentIndex = (currentIndex + 1) % gradients.length;
      }, 4000);
    }
  
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach((button) => {
      button.addEventListener('click', (event) => {
        if (!confirm('Tem certeza de que deseja excluir esta tarefa?')) {
          event.preventDefault();
        }
      });
    });
  
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach((input) => {
      input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
      });
      input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
      });
    });
  
    const tasks = document.querySelectorAll('.task');
    tasks.forEach((task) => {
      task.addEventListener('mouseenter', () => {
        task.style.transform = 'translateY(-5px)';
        task.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.1)';
      });
      task.addEventListener('mouseleave', () => {
        task.style.transform = 'translateY(0)';
        task.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
      });
    });
  });
  document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message) => {
      setTimeout(() => {
        message.style.transition = 'opacity 0.5s ease';
        message.style.opacity = '0';
        setTimeout(() => {
          message.remove();
        }, 500);
      }, 5000);
    });
  
    const header = document.querySelector('.header');
    if (header) {
      let startTime = null;
      const animateBackground = (timestamp) => {
        if (!startTime) startTime = timestamp;
        const progress = timestamp - startTime;
        const period = 4000;
        const factor = (Math.sin((progress / period) * 2 * Math.PI) + 1) / 2;
        const intensity = Math.floor(factor * 128);
        header.style.background = `rgb(${intensity}, ${intensity}, ${intensity})`;
        requestAnimationFrame(animateBackground);
      };
      requestAnimationFrame(animateBackground);
    }
  
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach((button) => {
      button.addEventListener('click', (event) => {
        if (!confirm('Tem certeza de que deseja excluir esta tarefa?')) {
          event.preventDefault();
        }
      });
    });
  
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach((input) => {
      input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
      });
      input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
      });
    });
  
    const tasks = document.querySelectorAll('.task');
    tasks.forEach((task) => {
      task.addEventListener('mouseenter', () => {
        task.style.transform = 'translateY(-5px)';
        task.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.1)';
      });
      task.addEventListener('mouseleave', () => {
        task.style.transform = 'translateY(0)';
        task.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
      });
    });
  });
  