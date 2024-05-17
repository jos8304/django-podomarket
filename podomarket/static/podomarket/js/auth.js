{
    const elt = document.querySelector('a.newreivew');

    function handleClick(e){
        if(!isAuthenticated){
            e.preventDefault();
            alert('로그인이 필요합니다.')
        }
    }

    elt.addEventListener('click', handleClick)
}