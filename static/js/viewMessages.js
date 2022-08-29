import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";

    const firebaseConfig = {
        apiKey: "AIzaSyCztAzrFHv3jenF6-uF9I92N-zp1v2Z80U",
        authDomain: "raspberry-9c43c.firebaseapp.com",
        databaseURL: "https://raspberry-9c43c-default-rtdb.firebaseio.com",
        projectId: "raspberry-9c43c",
        storageBucket: "raspberry-9c43c.appspot.com",
        messagingSenderId: "337910073952",
        appId: "1:337910073952:web:c6dd44debee759ffac9105"
    };

    const app = initializeApp(firebaseConfig);

    import {getDatabase, ref, child, onValue, get}
    from "https://www.gstatic.com/firebasejs/9.6.10/firebase-database.js"

    const db = getDatabase();

    var Nr = 0;
    var tbody = document.getElementById('tbody3');

    function AddItemToTable(Email, Nume, subiect, mesaj, Data){
        
        let trow = document.createElement("tr");
        let td1 = document.createElement('td');
        let td2 = document.createElement('td');
        let td3 = document.createElement('td');
        let td4 = document.createElement('td');
        let td5 = document.createElement('td');
        let td6 = document.createElement('td');
        td1.innerHTML = ++Nr;
        td2.innerHTML = Nume;
        td3.innerHTML = Email;
        td4.innerHTML = subiect;
        td5.innerHTML = mesaj;
        td6.innerHTML = Data;

        trow.appendChild(td1);
        trow.appendChild(td2);
        trow.appendChild(td3);
        trow.appendChild(td4);
        trow.appendChild(td5);
        trow.appendChild(td6);

        tbody.appendChild(trow);
    }

    function AddAllItemsToTable(Pacient){
        Nr = 0;
        tbody.innerHTML = "";
        Pacient.forEach(element =>{
            AddItemToTable(element.Pacient, element.Email, element.Subiect, element.Mesaj, element.Data);
        });
    }

    function GetAllDataOnce(){
        const dbRef = ref(db);

        get(child(dbRef, "Mesaje Pacienti"))
        .then((snapshot)=>{
            var pacient = [];

            snapshot.forEach(childSnapshot => {
                pacient.push(childSnapshot.val());
            });

            AddAllItemsToTable(pacient);
        });
    }

    window.onload = GetAllDataOnce;

function sortTableByColumn(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));
      
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
      
        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });
      
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }
      
    tBody.append(...sortedRows);
      
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-desc", !asc);
}
      
document.querySelectorAll(".table3-sortable th").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");
      
        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});

    