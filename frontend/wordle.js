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

    for (let i = 1; i <= maxCol; i++){
        let t = document.getElementById("tile".concat(i.toString()))
        t.addEventListener('click', function (event) {
            var currClass = t.className
            t.classList.remove(currClass);
            if (currClass === "empty")
                currClass = "correct";
            t.classList.add(classList[(classIndex[currClass] + 1) % 3]);
        });
    }
                
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
            for (let i = 1; i <= maxCol; i++){
                let t = document.getElementById("tile".concat(i.toString()))
                var currClass = t.className
                t.classList.remove(currClass);
                t.classList.add('empty')
                t.textContent = " ";
            }
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