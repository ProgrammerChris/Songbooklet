function opensidebar() {
    console.log("clicked open!")
    document.getElementById('rightside').style.display = 'grid';
    document.getElementById('rightside').style.gridTemplateRows = '9fr 1fr';
    document.body.style.display = 'grid';
    document.getElementById('showlistbutton').style.display = 'none'
    document.getElementById('hidelistbutton').style.display = 'block'
  }

function closesidebar() {
    document.getElementById('rightside').style.display = 'none';
    document.body.style.display = 'block';
    document.getElementById('showlistbutton').style.display = 'block'
    document.getElementById('hidelistbutton').style.display = 'none'
}
