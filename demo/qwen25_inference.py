#https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct

from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import json
import os
from tqdm import tqdm
import time
# default: Load the model on the available device(s)





def run_qwen25_coco(image_folder_dir,json_file,output_file,model_id):
    
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_id, torch_dtype="auto", device_map="auto"
)
    model.eval()

    processor = AutoProcessor.from_pretrained(model_id)


    responses = []


    with open(json_file) as f:
        data = json.load(f)
        for entry in tqdm(data,total=len(data)):

            model_responses = []
            img_id = entry.get("image_file")
            img_dir = f"{image_folder_dir}/{img_id}"
            # image = load_image(img_dir) 

            question_list = entry.get("questions")
            gpt_answer_list = entry.get("gpt_responses")


            print(f"Processing image {img_id}")
            for index, (question, gpt_answer) in enumerate(zip(question_list,gpt_answer_list)):



                messages = [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "image": f"file://{img_dir}",
                                    },
                                    {"type": "text", "text": question},
                                ],
                            }
                        ]
                # Preparation for inference
                #==============================================================================
                text = processor.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
                image_inputs, video_inputs = process_vision_info(messages)
                inputs = processor(
                    text=[text],
                    images=image_inputs,
                    videos=video_inputs,
                    padding=True,
                    return_tensors="pt",
                )

                inputs = inputs.to("cuda")

                # Inference: Generation of the output
                generated_ids = model.generate(**inputs, max_new_tokens=64)
                generated_ids_trimmed = [
                    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                
                output = processor.batch_decode(
                    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )
                #==============================================================================

                print(output[0])
                model_responses.append(output[0])

            responses.append({
            "img_id": img_id,
            "question": question_list,
            "model_response": model_responses,
            "gpt_answer": gpt_answer_list,
                })
    with open(output_file, 'w') as outfile:
        json.dump(responses, outfile, indent=4)




if __name__ == '__main__':
    # model_id = "Qwen/Qwen2.5-VL-3B-Instruct"
    # model_id = 'Qwen/Qwen2.5-VL-7B-Instruct'
    # model_id = "Qwen/Qwen2.5-VL-72B-Instruct"
    model_id = "Qwen/Qwen2.5-VL-32B-Instruct"

    image_folder_dir =  "" # path to COCO val2014 folder 
    json_file = "./question_set/VisualGenome1k_v1.json"
    output_name = model_id.split("/")[-1]

    output_file = f"inference_out/{output_name}.json" # path to your designated output folder

    run_qwen25_coco(image_folder_dir,json_file,output_file,model_id)