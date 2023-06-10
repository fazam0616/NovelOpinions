async function addBook(){
    let title = document.getElementById('title');
    let authors = document.getElementById('authors');
    let year = document.getElementById('year');
    let er = document.getElementById('error');
    let data = await fetch("/addBook",{
            method:"POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title:title.value,
                authors:authors.value.split(','),
                year:year.value
            })
        });


    data = await data.json()
    console.log(data);
    if (data.error==''){
        er.innerHTML = '';
        title.value='';
        authors.value='';
        year.value='';
        alert('Book Successfully Added')
    }else{
        er.innerHTML = data.error;
    }
}
