var SELECTED_QUESTION_ID = null;

$(document).ready(function() {

    $("#question_submit_button").click(function() {
        
        var questionInput_ = document.getElementById("question_input");
        var data = {
            "question_text": questionInput_.value
        }

        $.ajax({
            type: "POST",
            url: "/api/question",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function(data, textStatus, jqXHR) {
                console.log("question added");
                console.log(data);

                //unpack the id
                var questionId_ = data["question_id"];

                //create a question element
                /*
                <tr>
                    <td>To be or not to be?</td>
                    <td>
                        <button type="button" class="btn btn-default "><span class="glyphicon glyphicon-circle-arrow-right"></span> </button>
                        <button type="button" class="btn btn-danger"><span class="glyphicon glyphicon-remove"></span> </button>
                    </td>
                </tr>
                */
                var questionRow_ = document.createElement("tr");
                
                var questionText_ = document.createElement("td");
                questionText_.textContent = questionInput_.value;
                questionRow_.appendChild(questionText_);

                var actions_ = document.createElement("td");
                questionRow_.appendChild(actions_);

                //add the question element to the UI
                var questionList_ = document.getElementById("question_list");
                questionList_.insertBefore(questionRow_, questionList_.firstChild);
            },
            error: function() {
                console.log("question submit failed");
            },
            dataType: "json"
        });

    });

    $("button.question_select").click(function(event) {

        var cell_ = event.target.parentNode;

        //update the question text
        
        //get the text from the cell using getAttribute
        var questionText_ = cell_.getAttribute("data-value");
        console.log(questionText_);
        
        //fetch the p inside the blockquote using document.getElementById
        var questionTextElement_ = document.getElementById("selected_question_text");

        //set the textContent of the p as the question text
        questionTextElement_.textContent = questionText_; 

        //grab the id
        SELECTED_QUESTION_ID = cell_.getAttribute("data-id");

        //load the answers
    });

});

//text = request_body_json["question_text"]