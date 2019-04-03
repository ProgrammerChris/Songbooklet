
const LIST = {
    KEY: 'chosensongs',
    listOfSongs: new Map(),
    init()  {
        let _listOfSongs = sessionStorage.getItem(LIST.KEY);
        
        if (_listOfSongs)    {
            LIST.listOfSongs = JSON.parse(_listOfSongs);
            document.getElementById('sidemenu').innerHTML = ''; // Empties the list for redraw. VERY unefficient...
            for (let id in LIST.listOfSongs)  {
                addToSideMenu(id, LIST.listOfSongs[id][0], LIST.listOfSongs[id][1]);
            }
        }
    },
    async sync()    {
        await sessionStorage.setItem(LIST.KEY, JSON.stringify(LIST.listOfSongs));
    },
    addToList(elementId, artistname, songname)   {
        LIST.listOfSongs[elementId] = [artistname, songname]; // Adding to Object, not map, for some reason that won't work ?...
        LIST.sync();
    },
    createListItem(elementId, artistname, songname)   {
        let li = document.createElement('li');
        li.id = elementId + 'chosen';
        let container = document.createElement('container');
    
        let div = document.createElement('div');
        div.className = 'chosen';
    
        let song = document.createElement('p');
        song.className = 'songname';
        song.textContent = songname;
    
        let artist = document.createElement('p');
        artist.className = 'artistname';
        artist.textContent = artistname;
    
        let button = document.createElement('button');
        button.type = 'button';
        button.className = 'trashcan';
        button.onclick = function () {
            // If trashcan clicked, remove from list and removed from sessionstorage.
            document.getElementById('sidemenu').removeChild(document.getElementById(elementId + 'chosen'));
            delete LIST.listOfSongs[elementId];
            LIST.sync();
            };
    
        li.appendChild(container);
        container.appendChild(div);
        div.appendChild(song);
        div.appendChild(artist);
        li.appendChild(button);

        LIST.addToList(elementId, artistname, songname);

        return li;
    },
    inList(elementId)  {

        let listItems = document.querySelectorAll('#sidemenu li');
        for (let i = 0; i < listItems.length; i++) {
            if (listItems[i].id.includes(elementId))   {
                return true;
            }
        }
        return false;
    }

}

function addToSideMenu(elementId, artistname, songname)    {
    if (!LIST.inList(elementId)) {
        document.getElementById('sidemenu').appendChild(LIST.createListItem( elementId, 
                                                                            artistname, 
                                                                            songname)
                                                                            );
    }
}

// On backbutton pressed, refresh sidemenu.
 window.onpageshow = function(evt) {
     if (evt.persisted) {
         LIST.init();
     }
 };

LIST.init();
