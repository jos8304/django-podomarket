{
    const prevBtn = document.querySelector('.carousel .carousel-button.prev');
    const nextBtn = document.querySelector('.carousel .carousel-button.next');
    const images = document.querySelectorAll('.carousel img.image');


    let currIdx = 0;
    function handlePrevClick(e){
        if (currIdx > 0){
            images[currIdx].classList.add('hidden');
            currIdx--;
            images[currIdx].classList.remove('hidden'); 
        }
    }

    function handleNextClick(e){
        if (currIdx < images.length-1){
            images[currIdx].classList.add('hidden');
            currIdx++;
            images[currIdx].classList.remove('hidden'); 
        }
        
    }

    prevBtn.addEventListener('click', handlePrevClick)
    nextBtn.addEventListener('click', handleNextClick)
}

