document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('quantCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    let width, height;
    function resize() {
        const hero = document.querySelector('.hero');
        width = hero.offsetWidth;
        height = hero.offsetHeight;
        canvas.width = width;
        canvas.height = height;
    }
    
    window.addEventListener('resize', resize);
    setTimeout(resize, 50); // Ensure hero has rendered its full vh
    
    let time = 0;
    
    function draw() {
        // Clear frame but leave a slight trail for glowing effect
        ctx.fillStyle = 'rgba(15, 23, 42, 1)'; // Matches new dark theme bg completely to avoid smearing, or we use clearRect
        ctx.clearRect(0, 0, width, height);
        
        // Use 'screen' or 'lighter' blend mode for glowing lines
        ctx.globalCompositeOperation = 'screen';
        
        // Define our glowing strings (colors: Cyan, Purple, Green, Orange)
        // Opacity oscillates between 0.1 and 0.9 based on time to create a "fading/glowing" dynamic
        
        // String 1: Cyan (fast)
        const alpha1 = 0.5 + Math.sin(time * 0.02) * 0.4;
        drawWave(1.2, 0.008, 60, `rgba(6, 182, 212, ${alpha1})`, 0);
        
        // String 2: Purple (medium)
        const alpha2 = 0.5 + Math.sin(time * 0.015 + 2) * 0.4;
        drawWave(0.8, 0.005, 100, `rgba(168, 85, 247, ${alpha2})`, 100);
        
        // String 3: Green (slow)
        const alpha3 = 0.5 + Math.sin(time * 0.01 + 4) * 0.4;
        drawWave(1.5, 0.003, 40, `rgba(34, 197, 94, ${alpha3})`, 200);
        
        // String 4: Orange (erratic)
        const alpha4 = 0.5 + Math.sin(time * 0.025 + 6) * 0.4;
        drawWave(2.0, 0.01, 30, `rgba(249, 115, 22, ${alpha4})`, 300);
        
        ctx.globalCompositeOperation = 'source-over'; // Reset
        
        time += 1;
        requestAnimationFrame(draw);
    }
    
    function drawWave(frequency, speed, amplitude, color, phaseOffset) {
        ctx.beginPath();
        // Start from left side
        ctx.moveTo(0, height / 2);
        
        // Draw path across the screen
        for (let i = 0; i < width; i += 3) {
            // Complex wave combination to simulate a stochastic/quant model
            const baseWave = Math.sin((i * frequency * 0.002) + (time * speed) + phaseOffset);
            const secondaryWave = Math.cos((i * frequency * 0.005) - (time * speed * 0.5));
            const tertiaryWave = Math.sin((i * frequency * 0.001) + (time * speed * 0.2));
            
            // Map the wave vertically across the canvas
            const y = (baseWave * amplitude) + (secondaryWave * amplitude * 0.5) + (tertiaryWave * amplitude * 0.2) + (height / 2);
            
            ctx.lineTo(i, y);
        }
        
        // Apply glow properties
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.shadowBlur = 15;
        ctx.shadowColor = color;
        
        ctx.stroke();
        
        // Reset shadow so it doesn't affect other draws
        ctx.shadowBlur = 0;
    }
    
    // Start animation after layout
    setTimeout(() => {
        resize();
        draw();
    }, 100);
});
