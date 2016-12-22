$(document).ready(function() {
    var mainOutput = $('#output');
    var subOutput = $('#output2');
    var op = $('#operator');
    var num2 = $('#num2');
    var num1 = $('#num1');
    var temp = $('#temp');
    var clearData = function() {
        num1.val('');
        op.val('');
        num2.val('');
        temp.val('');
    };

    var clearOutput = function() {
        mainOutput.html('');
        subOutput.html('');
    };

    var digitError = function() {
        mainOutput.html('0');
        subOutput.html('Reach Digit Limit');
        temp.val(0);
    }

    $('.nums').click(function() {
        if (('+-*/').indexOf(mainOutput.html()) != -1) {
            mainOutput.html('');
        }
        // avoid multiple dot
        if ($(this).val() == '.' && (mainOutput.html()).indexOf('.') != -1) return ;
        if (mainOutput.html() == '0' || subOutput.html() == 'Reach Digit Limit') {
           clearOutput()
           //subOutput.html('');
        }

        if (temp.val() !== '') {
            clearOutput()
            clearData();
        }

        mainOutput.append($(this).val());
        subOutput.append($(this).val());

        if (mainOutput.html().length > 12) {
            digitError();
        }
    });

    $('#clearButton').click(function() {
        mainOutput.html('0');
        subOutput.html('');
        clearData();
    });

    $('#deleteButton').click(function() {
        if (mainOutput.html() != '0') {
            mainOutput.html(mainOutput.html().substring(0, mainOutput.html().length-1));
            subOutput.html(subOutput.html().substring(0, subOutput.html().length-1));
            if (mainOutput.html() == '') {
                mainOutput.html('0');
            }
        }
    });

    $('.btn-operate').click(function() {
    var newOperator = $(this).val();
    if (num1.val() !== '' &&  ('+-*/').indexOf(num1.val()) == -1 && op.val() !== '') {
          num2.val(mainOutput.html());
          if (('+-*/').indexOf(num2.val()) != -1) return ;
          var number1 = parseFloat(num1.val());
          var operator = op.val();
          var number2 = parseFloat(num2.val());
          var result;
          if (operator == '+') {
              result = number1 + number2;
          } else if (operator == '-') {
              result = number1 - number2;
          } else if (operator == '*') {
              result = number1 * number2;
          } else if (operator == '/') {
              result = parseFloat(number1 / number2);
          }

          if (result.toString().length > 12) {
              digitError();
          } else {
              mainOutput.html(newOperator);
              subOutput.html(result + newOperator);
              num1.val(result);
              op.val(newOperator);
          }
    } else {
        num1.val(mainOutput.html());
        op.val(newOperator);
        mainOutput.html(newOperator);
        subOutput.append(newOperator);
    }
    });

    $('#resultButton').click(function() {
       if (mainOutput.html() === '' || ('+-*/').indexOf(mainOutput.html()) != -1) return ;
        num2.val(mainOutput.html());
        var number1 = parseFloat(num1.val());
        var operator = op.val();
        var number2 = parseFloat(num2.val());
        var result;
        if (operator == '+') {
            result = number1 + number2;
        } else if (operator == '-') {
            result = number1 - number2;
        } else if (operator == '*') {
            result = number1 * number2;
        } else if (operator == '/') {
            result = parseFloat(number1 / number2);
        }
        if (result.toString().length > 12) {
            digitError();
        } else {
            mainOutput.html(result);
            subOutput.html('');
            temp.val(result);
        }
    });
});