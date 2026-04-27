function increment() {
        const result = document.getElementById('result');
        let value = parseInt(result.textContent);

        value = value + 1;
        result.textContent = value;
    }

    function decrement() {
        const result = document.getElementById('result');
        let value = parseInt(result.textContent); //문자를 읽어서 숫자로 바꾼다.

        value = value - 1;
        result.textContent = value;
    }

    const button1 = document.getElementById('incButton'); 
    const button2 = document.getElementById('decButton');

    /* 이벤트 핸들러 */
    button1.addEventListener('click', increment);
    button2.addEventListener('click', decrement);

    //이 코드를 간소화 시키면 강사님 Github 코드가 됨.