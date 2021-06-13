const showFrenchTitle = document.querySelector(".js-show-french-title");
if (showFrenchTitle) {
    showFrenchTitle.addEventListener("click", function (event) {

        if (showFrenchTitle.checked) {
            showOriginalTitle();
        } else {
            showTitle();
        }

        function showOriginalTitle() {
            document.querySelectorAll(".js-original-title").forEach(function (el) {
                el.style.display = "none";
            });

            document.querySelectorAll(".js-title").forEach(function (el) {
                el.style.display = "inline";
            });
        }

        function showTitle() {
            document.querySelectorAll(".js-original-title").forEach(function (el) {
                el.style.display = "inline";
            });

            document.querySelectorAll(".js-title").forEach(function (el) {
                el.style.display = "none";
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
