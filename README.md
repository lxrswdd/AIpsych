# AIpsych
### Towards a Psychoanalytic Perspective on VLM Behaviour: A First-step Interpretation with Intriguing Observations


Hallucination is a long-standing problem that has been actively investigated in Vision-Language Models (VLMs). Existing research commonly attributes hallucinations to technical limitations or sycophancy bias, where the latter means the models tend to generate incorrect answers to align with user expectations. However, these explanations primarily focus on technical or externally driven factors, may have neglected the possibility that hallucination behaviours might mirror cognitive biases observed in human psychology.  In this work, we introduce a psychological taxonomy, categorizing VLMs' hallucination behaviours, including sycophancy, logical inconsistency, and a newly identified VLMs behaviour: authority bias. To systematically analyze these behaviours, we design AIpsych, a scalable benchmark that reveals psychological tendencies in model response patterns. Leveraging this benchmark, we investigate how variations in model architecture and parameter size influence model behaviour when responding to strategically manipulated questions. Our experiments reveal that as model size increases, VLMs exhibit stronger sycophantic tendencies but reduced authority bias, suggesting increasing competence but a potential erosion of response integrity. A human subject study further validates our hypotheses and highlights key behavioural differences between VLMs and human respondents. This work suggests a new perspective for understanding hallucination in VLMs and highlights the importance of integrating psychological principles into model evaluation.


<div align="center">
    <img src='img/ques_tree.png'/>
</div>



## 📜 News

**[2025/7/7]** Version 1 released.


## 🎈 Quick Start

### Inference the Qwen2.5VL with the AIpsych - COCO valid 2014 dataset
```
python /demo/qwen25_inference.py
```

### Evaluate the results 
```
python AIpysch_evaluation_v1.py --input_json "Your path to the Qwen2.5VL inference results"
```

