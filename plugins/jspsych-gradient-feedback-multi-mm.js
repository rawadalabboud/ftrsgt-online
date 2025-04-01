/**
 * jspsych-gradient-feedback-mm
 *
 */

const isString = value => typeof value === "string" || value instanceof String;

jsPsych.plugins['gradient-feedback-multi-mm'] = (function () {

    var plugin = {};

    jsPsych.pluginAPI.registerPreload('gradient-feedback-multi-mm', 'stimuli', 'image');

    plugin.info = {
        name: 'gradient-feedback-multi-mm',
        description: '',
        parameters: {
            titles: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'array of titles for subscales',
                default: Array(),
                description: 'An array of strings with titles for each sub-scale'
            },
            start_colors: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'Start color(s)',
                default: "black",
                description: 'Array of colors for starting the gradient (or single name of color).'
            },
            end_colors: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'End color(s)',
                default: "red",
                description: 'Array of colors for ending the gradient (or single name of color).'
            },            
            left_labels: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'Left anchor for scales',
                default: "low",
                description: 'Can be any valid HTML, also an image.'
            },
            right_labels: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'Right anchor for scales',
                default: "high",
                description: 'Can be any valid HTML, also an image.'
            },
            values: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'Values for feedback',
                default: Array(),
                description: 'Array of values for feedback as numbers between 0 and 100.'
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
            opacities: {
                type: jsPsych.plugins.parameterType.OBJECT,
                pretty_name: 'Opacities for the scales (to grey out individual ones).',
                default: 1,
                description: 'Array of opacity-values for the scales or a single number bw 0 and 1.'
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
        var nscales=trial.values.length;

        if(isString(trial.start_colors)){
            trial.start_colors=Array(nscales).fill(trial.start_colors);
        }
        if(isString(trial.end_colors)){
            trial.end_colors=Array(nscales).fill(trial.end_colors);
        }
        if(isString(trial.left_labels)){
            trial.left_labels=Array(nscales).fill(trial.left_labels);
        }
        if(isString(trial.right_labels)){
            trial.right_labels=Array(nscales).fill(trial.right_labels);
        }
        if(typeof trial.opacities==="number"){
            trial.opacities=Array(nscales).fill(trial.opacities);
        }

        var html = "";


        html += `<div style="display:grid;text-align:center;
                             grid-template-columns: 80px ${ trial.width }px 80px;
                             row-gap:0px;
                             column-gap:40px;">
        `
        for(let i=0; i<nscales; i++){
            html+=`
            <div style="height:${ trial.height };
                        width:${ trial.height };
                        opacity:${ trial.opacities[i] };">
                ${ trial.left_labels[i] }
            </div>
            <div id="gradient-box" class="jspsych-gradient-box" style="
                 width:${ trial.width }px;
                 height:${ trial.height }$;
                 margin:auto; 
                 text-align:left;
                 border: 2px solid black;
                 display: flex;
                 background:linear-gradient(to right,${ trial.start_colors[i] },${ trial.end_colors[i] });
                 opacity:${ trial.opacities[i] };
                 ">
                <div style="background:#00000000;
                            height:${ trial.height };
                            width:${ ((trial.values[i]/100.)*trial.width) }px;
                            opacity:${ trial.opacities[i] };"></div>
                <div style="background:grey;
                            height:${ trial.height };
                            width:${ (trial.width-(trial.values[i]/100.)*trial.width) }px;
                            font-color:white; 
                            font-size:40px; 
                            text-align: left;
                            line-height:${ trial.height };
                            opacity:${ trial.opacities[i] };">
                    ${ trial.values[i] } 
                </div>                            
            </div>
            <div style="height:${ trial.height };
                        width:${ trial.height };
                        opacity:${ trial.opacities[i] };">
                ${ trial.right_labels[i] }
            </div>

            <div style="height:40px;opacity:${ trial.opacities[i] };"></div> 
            <div style="opacity:${ trial.opacities[i] };">${ trial.titles[i] }</div>
            <div></div> 
            `

        }
        html+=`</div><p style="height:30px">`
        /*
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
        */
        display_element.innerHTML = html;
        // add button
        display_element.innerHTML += '<button id="jspsych-gradient-continue-btn" class="jspsych-btn">' + trial.button_label + '</button>';

        // clicking the button will stop training
        display_element.querySelector('#jspsych-gradient-continue-btn').addEventListener('click', function (e) {
            end_trial();
        })

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
                "fb_value": trial.values,
                "fb_title": trial.titles,
                "rt": performance.now()-start_time
            };

            // clear the display
            display_element.innerHTML = '';

            // move on to the next trial
            jsPsych.finishTrial(trial_data);
        };
    };


    return plugin;
})();
