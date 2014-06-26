function selectQuestion() {

    //fetch the p inside the blockquote using document.getElementById
    var questionTextElement_ = document.getElementById("selected_question_text");

    //set the textContent of the p as the question text
    questionTextElement_.textContent = SELECTED_QUESTION_TEXT;

    

    //load the answers


};

$(document).ready(function() {

    $("#question_submit_button").click(function(event) {
        
        var questionSubmitButton_ = event.target;
        var questionInput_ = document.getElementById("question_input");
        var data = {
            "question_text": questionInput_.value
        }

        questionSubmitButton_.setAttribute("disabled", "disabled");
        questionInput_.setAttribute("disabled", "disabled");

        $.ajax({
            type: "POST",
            url: "/api/question",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function(data, textStatus, jqXHR) {

                //only run if on our drafts page
                if(QUESTION_FILTER == "draft") {
                    //unpack the id
                    var questionId_ = data["question_id"];

                    //create a question element
                    var questionRow_ = document.createElement("tr");
                
                    var questionText_ = document.createElement("td");
                    questionText_.textContent = questionInput_.value;
                    questionRow_.appendChild(questionText_);

                    var actions_ = document.createElement("td");
                    questionRow_.appendChild(actions_);

                    //add the question element to the UI
                    var questionList_ = document.getElementById("question_list");
                    questionList_.insertBefore(questionRow_, questionList_.firstChild);

                    SELECTED_QUESTION_ID = questionId_;
                    SELECTED_QUESTION_TEXT = questionInput_.value;

                    selectQuestion();
                }

                questionInput_.value = "";
                questionSubmitButton_.removeAttribute("disabled");
                questionInput_.removeAttribute("disabled");
            },
            error: function() {
                console.log("question submit failed");
            },
            dataType: "json"
        });

    });
    

    $("button.question_select").click(function(event) {

        var cell_ = event.target.parentNode;
        //grab the id
        SELECTED_QUESTION_ID = cell_.getAttribute("data-id");
        SELECTED_QUESTION_TEXT = cell_.getAttribute("data-value");

        selectQuestion();
    });

    $("button.question_delete").click(function(event) {

        var cell_ = event.target.parentNode;
        var questionId_ = cell_.getAttribute("data-id");

        $.ajax({
            type: "DELETE",
            url: "/api/question/"+questionId_,
            contentType: "application/json; charset=utf-8",
            success: function(data, textStatus, jqXHR) {

                //get rid of the question row
                var questionRow_ = cell_.parentNode;
                var questionList_ = questionRow_.parentNode;
                questionList_.removeChild(questionRow_);

                //if this row was select, select a new question


            },
            error: function() {
                console.log("question question failed");
            }
        });
    });

    $("#answer_submit_button").click(function(event) {
        
        var answerSubmitButton_ = event.target;
        var answerInput_ = document.getElementById("submit_answer_text");
        var answerComment = document.getElementById("submit_comment");
        var answer_ = {
            "answer_text": answerInput_.value,
            "answer_comment": answerComment.value
        }

        answerSubmitButton_.setAttribute("disabled", "disabled");
        answerInput_.setAttribute("disabled", "disabled");

        $.ajax({
            type: "POST",
            url: "/api/question/"+SELECTED_QUESTION_ID+"/answer",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(answer_),
            success: function(data, textStatus, jqXHR) {

                var answerRow_ = document.createElement("tr");

                var answerRank_ = document.createElement("td");
                answerRow_.appendChild(answerRank_);

                var answerVotes_ = document.createElement("td");
                answerRow_.appendChild(answerVotes_);

                var answerImg_ = document.createElement("td");
                answerRow_.appendChild(answerImg_);
          
                var answerText_ = document.createElement("td");
                answerText_.textContent = answerInput_.value;
                answerRow_.appendChild(answerText_);

                var answerActions_ = document.createElement("td");
                answerRow_.appendChild(answerActions_);

                var answerList_ = document.getElementById("answer_list");
                answerList_.appendChild(answerRow_);

                answerInput_.value = "";
                answerComment.value = "";
                answerSubmitButton_.removeAttribute("disabled");
                answerInput_.removeAttribute("disabled");
            },
            error: function() {
                console.log("answer submit failed");
            },
            dataType: "json"
        });

    });

    //perform first load
    if(SELECTED_QUESTION_ID != null) {
        selectQuestion();
    }

});