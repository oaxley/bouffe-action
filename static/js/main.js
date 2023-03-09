/*
 * @brief   main.js
 * @author  Sebastien LEGRAND
 * @date    2023-03-08
 *
 * @brief   Main Javascript file for "Bouffe Action" collector
 */

//----- constants

// flask endpoint
const SERVER_URL="http://localhost:5000/api/v1"

const SCALE_TIMER_INTERVAL_MS = 2000;
const INPUT_FOCUS_INTERVAL_MS = 1000;

const BARCODE_PROVIDER_MARKER = 'F';
const BARCODE_PRODUCT_MARKER = 'P';


//----- globals

var last_provider = "";
var last_weight = 0.0;

var last_items = 1;


//----- functions
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function animateEntry(ms) {
    var entry = document.getElementById("barcode-entry");
    var old_style = entry.className;

    entry.className = entry.className + " bg-danger text-white";
    sleep(ms).then(() => {
        entry.className = old_style;
    });
}

// setup the page
function setup() {
    // setup the scale monitoring every seconds or so
    setInterval(readScaleValue, SCALE_TIMER_INTERVAL_MS);

    setInterval(setInputFocus, INPUT_FOCUS_INTERVAL_MS)

    // bind the enter key to the barcode button
    window.addEventListener("keypress", (event) => {
        if (event.key == "Enter") {
            document.getElementById("barcode-btn").click();
        }
    });
}

// reset focus to input field
function setInputFocus() {
    var inputBar = document.getElementById("barcode-entry");
    if(document.activeElement != inputBar) {
        inputBar.focus()
    }
}


// read the scale value
function readScaleValue() {
    fetch(SERVER_URL + "/scale")
    .then((response) => {
        return response.json();
    })
    .then((json) => {
       var element = document.getElementById("current-weight");
       element.innerHTML = json['value'];
       last_weight = json['value'];
    })
    .catch(() => {
        console.log("Unable to retrieve the value of the scale!");
    });
}

// read the entry from the user
function readEntry() {
    var entry = document.getElementById("barcode-entry");

    switch (entry.value.charAt(0)) {
        case BARCODE_PROVIDER_MARKER:
            retrieveProvider(entry.value);
            break;
        case BARCODE_PRODUCT_MARKER:
            retrieveProduct(entry.value);
            break;
        default:
            console.log('Meh?');
            break;
    }
}

// retrieve the entity name
function retrieveProvider(eid) {
    fetch(SERVER_URL + "/entity/" + eid)
    .then((response) => {
        if (response.status != 200) {
            // do a little animation to notify the user
            animateEntry(200);
            throw 'cancel';
        } else {
            return response.json();
        }
    })
    .then((json) => {
        var provider = document.getElementById("last-provider");
        provider.innerHTML = json['ename'];
        last_provider = json['ename'];

        var entry = document.getElementById("barcode-entry");
        entry.value = "";
    })
    .catch(() => {
        return "";
    });
}

// retrieve the product
function retrieveProduct(eid) {
    fetch(SERVER_URL + "/entity/" + eid)
    .then((response) => {
        if (response.status != 200) {
            // do a little animation to notify the user
            animateEntry(200);
            throw 'cancel';
        } else {
            return response.json();
        }
    })
    .then((json) => {
        var entry = document.getElementById("barcode-entry");

        if (last_provider == "") {
            entry.value = "";
            return;
        }

        addTableEntry(last_provider, json['ename'], last_weight);
        entry.value = "";
    })
    .catch(() => {
        return "";
    });

}

// add a new entry in the table
function addTableEntry(provider, product, weight) {
    // send the item to the backend
    fetch(SERVER_URL + "/input", {
        method: "POST",
        body: JSON.stringify({
            provider: provider,
            product: product,
            weight: weight
        }),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => {
        return response.json()
    })
    .then((json) => {
        // the json contains the ID of the item
        var id = json['id']

        // create a new entry in the table
        var table = document.getElementById("table-content");
        var x = table.rows.length;
        var row = table.insertRow(x);

        // add the data to the table
        row.id = id;
        row.insertCell(0).innerHTML = `<th scope="row">${last_items}</th>`;
        row.insertCell(1).innerHTML = provider;
        row.insertCell(2).innerHTML = product;
        row.insertCell(3).innerHTML = weight;
        row.insertCell(4).innerHTML = '<input type="button" class="btn btn-danger btn-sm" id="delrow" onclick="deleteRow(\''+id+'\')" value="Supprimer" />';

        // increment the number of items
        last_items = last_items + 1;
    });
}


function deleteRow(id) {
    /* remove the item from the backend first */
    fetch(SERVER_URL + "/input/" + id, {
        method: "DELETE"
    })
    .then((response) => {
        return response.json()
    })
    .then((json) => {
        document.getElementById(id).remove();
    });
}


//----- begin
setup();