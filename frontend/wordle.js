const classList = ["absent", "present", "correct"];

var classIndex = {"absent": 0,
                 "present": 1,
                 "correct": 2}; 
let col = 1;
let maxCol = 5;


window.onload = function(){
    intialize();
}

function intialize() {
    let t1 = document.getElementById('tile1');
    t1.addEventListener('click', function (event) {
        var currClass = t1.className
        t1.classList.remove(currClass);
        if (currClass === "empty")
            currClass = "correct";
        t1.classList.add(classList[(classIndex[currClass] + 1) % 3]);
    });

    let t2 = document.getElementById('tile2');
    t2.addEventListener('click', function (event) {
        var currClass = t2.className
        t2.classList.remove(currClass);
        if (currClass === "empty")
            currClass = "correct";
        t2.classList.add(classList[(classIndex[currClass] + 1) % 3]);
    });

    let t3 = document.getElementById('tile3');
    t3.addEventListener('click', function (event) {
        var currClass = t3.className
        t3.classList.remove(currClass);
        if (currClass === "empty")
            currClass = "correct";
        t3.classList.add(classList[(classIndex[currClass] + 1) % 3]);
    });

    let t4 = document.getElementById('tile4');
    t4.addEventListener('click', function (event) {
        var currClass = t4.className
        t4.classList.remove(currClass);
        if (currClass === "empty")
            currClass = "correct";
        t4.classList.add(classList[(classIndex[currClass] + 1) % 3]);
    });

    let t5 = document.getElementById('tile5');
    t5.addEventListener('click', function (event) {
        var currClass = t5.className
        t5.classList.remove(currClass);
        if (currClass === "empty")
            currClass = "correct";
        t5.classList.add(classList[(classIndex[currClass] + 1) % 3]);
    });

    let keyboardRows = document.getElementsByClassName('keyboardRow');
    
    
    for (let i = 0; i < keyboardRows.length; i++) {
        let currRow = keyboardRows[i].children;
        
        for (let j = 0; j < currRow.length; j++) {
            let key = currRow[j]
            
            key.addEventListener('click', processKey)
        }
    }

    document.addEventListener("keyup", (e) => {
    processInput(e);
    })
}


function processKey() {
    e = { "code" : this.id };
    processInput(e);
}

function processInput(e) {

    if ("KeyA" <= e.code && e.code <= "KeyZ") {
        if (col <= maxCol){
            let specifiedTile = document.getElementById("tile".concat(col.toString()));              
            specifiedTile.textContent = e.code[3]
            col++;
        }
    }
    else if (e.code == "Backspace") {
        if (col>1){
            let specifiedTile = document.getElementById("tile".concat((col-1).toString()));              
            specifiedTile.textContent = " "
            col--;
        }
    }
    else if (e.code == "Restart") {
        location.reload();
    }
    else if (e.code == "Enter") {
        let patternEntered = true;
        for (let i = 1; i <= maxCol; i++){
                if (document.getElementById("tile".concat(i.toString())).className === "empty")
                    patternEntered = false;    
        }
        
        if (col-1 == 5 && patternEntered){
            let updateMes = document.getElementById("updateMessage").children[0];
            updateMes.textContent = "";

            let t1 = document.getElementById('tile1');
            var currClass = t1.className
            t1.classList.remove(currClass);
            t1.classList.add('empty')

            let t2 = document.getElementById('tile2');
            var currClass = t2.className
            t2.classList.remove(currClass);
            t2.classList.add('empty')

            let t3 = document.getElementById('tile3');
            var currClass = t3.className
            t3.classList.remove(currClass);
            t3.classList.add('empty')

            let t4 = document.getElementById('tile4');
            var currClass = t4.className
            t4.classList.remove(currClass);
            t4.classList.add('empty')

            let t5 = document.getElementById('tile5');
            var currClass = t5.className
            t5.classList.remove(currClass);
            t5.classList.add('empty')

            for (let i = 1; i <= maxCol; i++)
                document.getElementById("tile".concat(i.toString())).textContent = " ";
            col = 1;
            // Send to python app
            // Display results
            let resultSection = document.getElementById("resultsWrapper");
            resultSection.classList.remove("hidden");
            resultSection.classList.add("visible");
            
        }
        else {
            let updateMes = document.getElementById("updateMessage").children[0];
            if (patternEntered)
                updateMes.textContent = "Please enter a 5 letter word.";
            else
                updateMes.textContent = "The pattern specified is invalid.";
        }
    }
}