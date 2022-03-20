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

function getPatternCode(color) {
    return classIndex[color].toString();
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
        $.post( "/restart", { });
        location.reload();
    }
    else if (e.code == "Enter") {
        let patternEntered = true;
        for (let i = 1; i <= maxCol; i++){
                if (document.getElementById("tile".concat(i.toString())).className === "empty")
                    patternEntered = false;    
        }
        
        if (col-1 == 5 && patternEntered){
            let guess = "";
            let pattern = "";
            let updateMes = document.getElementById("updateMessage").children[0];
            updateMes.textContent = "";
            
            let alterMes = document.getElementById("alert");
            alterMes.textContent = "LOADING..."
            let ranks = document.getElementsByClassName('rank')
            let guesses = document.getElementsByClassName('guess')
            let bitss = document.getElementsByClassName('bits')
            for (let j=0; j<3; j++){
                ranks[j].textContent = "";
                guesses[j].textContent = "";
                bitss[j].textContent = "";
                
            }
            
            for (let i = 1; i <= maxCol; i++){
                let t = document.getElementById("tile".concat(i.toString()))
                var currClass = t.className
                t.classList.remove(currClass);
                t.classList.add('empty')
                pattern += getPatternCode(currClass);
                guess += t.textContent.toString();
                t.textContent = " ";
                
            }
            col = 1;

            // Send to python app
            console.log(guess);
            $.post( "/", {
                userGuess: guess,
                userPattern: pattern 
            });
            console.log(pattern);
            // Display results
            let resultSection = document.getElementById("resultsWrapper");
            
            $.get("/getpythondata", function(data) {
                
                let myres = $.parseJSON(data)
                console.log(myres);

                let total = 0;
                console.log(total);
                for (var i in myres){
                    total++;
                }
                console.log(total);
                if (total === 1){
                    for (var i in myres)
                        guesses[0].textContent = "The answer is " + myres[i][0].toUpperCase() + "!";
                        guesses[1].textContent = "Hit RESTART, or wait and this page will automatically refresh.";
                        $.post( "/restart", { });
                        setTimeout(function(){location.reload();}, 8000);
                }
                else{
                    let count = 0;
                    for (var i in myres){
                        let w = myres[i][0];                
                        let r = myres[i][1].toString();

                        ranks[count].textContent = (count+1).toString()+'.';
                        guesses[count].textContent = w.toUpperCase();
                        bitss[count].textContent = r.substr(0,5) + " Bits";
                        
                        count = count + 1;
                    }
                }
                let alterMes = document.getElementById("alert");
                alterMes.textContent = "";
                
                //alterMes.classList.remove("visible");
                //alterMes.classList.add("hidden");
                //if (data === 'congrats!'){
                  //  setTimeout(function(){location.reload();}, 3000);

            })
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
