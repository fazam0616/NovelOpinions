async function searchBooks(){
    let title = document.getElementById('title');
    let author = document.getElementById('author');
    let start = document.getElementById('start');
    let end = document.getElementById('end');
    let er = document.getElementById('error');
    let partial = document.getElementById('partial');
    let data = await fetch("/searchBook",{
            method:"POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title:title.value,
                author:author.value,
                start:start.value,
                end:end.value,
                partial:partial.checked
            })
        });


    data = await data.json()
    console.log(data);

    if (data.error==''){

    }else{
        er.innerHTML = data.error;
    }
}
