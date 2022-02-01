function like(postId){
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    //Envia uma requisição
    fetch(`/like-post/${postId}`, {method: "POST"}).then((res) => res.json()).then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true){
            likeButton.className = "fas fa-thumbs-up";
        }
        else{
            likeButton.className = "far fa-thumbs-up";
        }
    }).catch((e) => alert('Não é possível curtir a postagem!'));
}