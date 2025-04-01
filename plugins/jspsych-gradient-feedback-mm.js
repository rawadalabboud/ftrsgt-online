/**
 * jspsych-gradient-feedback-mm
 *
 */


jsPsych.plugins['gradient-feedback-mm'] = (function () {

    var plugin = {};

    jsPsych.pluginAPI.registerPreload('gradient-feedback-mm', 'stimuli', 'image');

    plugin.info = {
        name: 'gradient-feedback-mm',
        description: '',
        parameters: {
            title: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'title for the scale',
                default: "",
                description: 'A title/label put under the scale.'
            },
            start_color: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Start color',
                default: "black",
                description: 'Color for starting the gradient.'
            },
            end_color: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'End color',
                default: "red",
                description: 'Color to end the gradient.'
            },
            left_label: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Left anchor for scale',
                default: "low",
                description: 'Can be any valid HTML, also an image.'
            },
            right_label: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Right anchor for scale',
                default: "high",
                description: 'Can be any valid HTML, also an image.'
            },
            value: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Value for feedback',
                default: 0,
                description: 'Value for feedback as number between 0 and 100.'
            },
            width: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Width of feedback box',
                default: 700,
                description: 'Width of feedback box in pixels.'
            },
            height: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Height of feedback box',
                default: "80px",
                description: 'Height of feedback box in CSS style (e.g., 500px or 20%).'
            },
            button_label: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Button label',
                default: 'Continue',
                description: 'The text that appears on the button to continue to the next trial.'
            }
        }
    }

    plugin.trial = function (display_element, trial) {
        var start_time = performance.now();

        var html = "";

        /*
        html += '<p style="margin-bottom:80px">'+
            '<div id="gradient-box-val" class="jspsych-gradient-box-val" style="'+
            'background:#00000055;'+
            'height:'+trial.height+';'+
            'width:'+trial.width+'px;'+
            'font-color:white;font-size:40px;text-align: left;'+
            'line-height:'+trial.height+';'+
            '">'+
            '<div id="gradient-box" class="jspsych-gradient-box" style="'+
            'width:'+(trial.value/100.)*trial.width+'px;height:'+trial.height+';'+
            'margin:auto;text-align:left;'+
            'background:linear-gradient(to right,'+trial.start_color+','+trial.end_color+');'+
            '">'+
            trial.value+
            '</div>'+
            '</div><p>';
        */
        html += '<div style="display:grid;text-align:center;'+ //height:'+trial.height+';'+
            'line-height:'+trial.height+';'+
            'grid-template-columns: 80px '+trial.width+'px 80px;'+
            'column-gap:40px;'+
            '">'+
            trial.left_label+
            '<div id="gradient-box" class="jspsych-gradient-box" style="'+
            'width:'+trial.width+'px;height:'+trial.height+';'+
            'margin:auto;text-align:left;border: 2px solid black;'+
            'display: flex;'+
            'background:linear-gradient(to right,'+trial.start_color+','+trial.end_color+');'+
            '">'+      
            '<div style="'+
            'background:#00000000;'+
            'height:'+trial.height+';'+
            'width:'+((trial.value/100.)*trial.width)+'px;'+
            '"></div>'+                  
            '<div style="'+
            'background:grey;'+
            'height:'+trial.height+';'+
            'width:'+(trial.width-(trial.value/100.)*trial.width)+'px;'+
            'font-color:white;font-size:40px;text-align: left;'+
            'line-height:'+trial.height+';'+
            '">'+
            trial.value+
            '</div>'+
            '</div>'+
            trial.right_label+
            '<div></div><div style="font-size:30px">'+
            trial.title+
            '</div><div></div></div>'+
            '</div>'+
            '<p style="height:30px">';
            //'<div style="font-size:30px">'+trial.value+'</div>'+
            //'<p>';

        display_element.innerHTML = html;
        // add button
        display_element.innerHTML += '<button id="jspsych-gradient-continue-btn" class="jspsych-btn">' + trial.button_label + '</button>';

        // clicking the button will stop training
        display_element.querySelector('#jspsych-gradient-continue-btn').addEventListener('click', function (e) {
            end_trial();
        })

        var target=display_element.querySelector('#jspsych-gradient-box');

        // function to end trial when it is time
        var end_trial = function () {

            // kill any remaining setTimeout handlers
            jsPsych.pluginAPI.clearAllTimeouts();

            // kill keyboard listeners
            if (typeof keyboardListener !== 'undefined') {
                jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
            }

            // gather the data to store for the trial
            var trial_data = {
                "training_type": trial.training_type,
                "rt": performance.now()-start_time
            };

            // clear the display
            display_element.innerHTML = '';

            // move on to the next trial
            jsPsych.finishTrial(trial_data);
        };

        // function to highlight box corresponding to each key
        var after_response = function (info) {
            var keypressed=jsPsych.pluginAPI.convertKeyCodeToKeyCharacter(info.key)
        };


        // start the response listener that highlights individual rectangles
        var keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
            callback_function: after_response,
            valid_responses: jsPsych.ALL_KEYS,
            rt_method: 'performance',
            persist: true,
            allow_held_key: false
        });
    };


    return plugin;
})();
