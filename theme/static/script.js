const showFrenchTitle = document.querySelector(".js-show-french-title");
if (showFrenchTitle) {
    showFrenchTitle.addEventListener("click", function (event) {
        console.log(showFrenchTitle.checked)
        if (showFrenchTitle.checked) {
            showOriginalTitle();
        } else {
            showTitle();
        }

        function showOriginalTitle() {
            document.querySelectorAll(".js-original-title").forEach(function (el) {
                el.style.display = "inline";
            });

            document.querySelectorAll(".js-title").forEach(function (el) {
                el.style.display = "none";
            });
        }

        function showTitle() {
            document.querySelectorAll(".js-original-title").forEach(function (el) {
                el.style.display = "none";
            });

            document.querySelectorAll(".js-title").forEach(function (el) {
                el.style.display = "inline";
            });
        }
    });
}


function sortTable(table, col, reverse) {
    var tb = table.tBodies[0], // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
        tr = Array.prototype.slice.call(tb.rows, 0), // put rows into array
        i;

    reverse = ((+reverse) || -1);
    tr = tr.sort(function (a, b) { // sort rows
        if (a.cells[col].hasAttribute("data-sort-value")) {
            return reverse // `-1 *` if want opposite order
                * (a.cells[col].getAttribute("data-sort-value")
                    .localeCompare(b.cells[col].getAttribute("data-sort-value"), undefined, { numeric: true })
                );
        }

        return reverse // `-1 *` if want opposite order
            * (a.cells[col].textContent.trim() // using `.textContent.trim()` for test
                .localeCompare(b.cells[col].textContent.trim())
            );
    });
    for (i = 0; i < tr.length; ++i) tb.appendChild(tr[i]); // append each row in order
}

function makeSortable(table) {
    var th = table.tHead, i;
    th && (th = th.rows[0]) && (th = th.cells);
    if (th) i = th.length;
    else return; // if no `<thead>` then do nothing
    while (--i >= 0) (function (i) {
        var dir = 1;
        th[i].addEventListener('click', function () { sortTable(table, i, (dir = 1 - dir)) });
    }(i));
}

const table = document.querySelector(".js-sort-table");
if (table) {
    makeSortable(table);
}

// Review toggle
const expandables = document.querySelectorAll(".js-expandables");
expandables.forEach(expandable => {
    expandable.addEventListener("click", reviewToggle);
});

function reviewToggle(event) {
    const target = event.target;

    let id = "";
    let row = target.parentNode;

    while (true) {
        if (row.dataset.movieId != null || undefined) {
            id = row.dataset.movieId;
            break;
        }
        row = row.parentNode;
    }

    toggleRow(id);
    toggleFragment(id);
}

function toggleRow(id) {
    let node = document.querySelector('[data-expands-for="' + id + '"]');
    node.classList.toggle("dn");
    node.classList.toggle("db");
    node.classList.toggle("dt-row-l");
}

function toggleFragment(id) {
    if (window.location.hash.includes(id)) {
        // https://stackoverflow.com/questions/1397329/how-to-remove-the-hash-from-window-location-url-with-javascript-without-page-r/5298684#5298684
        history.pushState("", document.title, window.location.pathname + window.location.search);
    } else {
        window.location.hash = id;
    }
}
