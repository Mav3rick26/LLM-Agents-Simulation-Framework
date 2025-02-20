# 🤖 *A simulation framework designed to study complex social dynamics using generative agents powered by LLMs*
[![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This repository contains a **Generative Agent-Based Modeling (GABM)** framework that integrates **Large Language Models (LLMs)** into *agent-based simulations*. It enables the study of emergent social behaviors in complex environments such as social networks, content virality, and opinion dynamics.

## 🔍 Framework Overview
This framework adopts a modular, phase-based approach to simulate and analyze interactions within a social environment. The simulation workflow is divided into several phases, each contributing to the realistic modeling of agent interactions. Agents dynamically evolve within the simulated social network, making autonomous decisions based on memory, personality, and environmental feedback. More details can be found in our published papers cited below.

<img src="https://github.com/user-attachments/assets/5a86c3b2-a872-4d9e-a33f-1a0dbffed032" alt="Workflow" width="750">

## 🛠 Technologies Used
- **Python**: Core programming language ([Python](https://www.python.org/))
- **PyAutogen**: LLM-powered agent automation ([PyAutogen](https://github.com/microsoft/autogen))
- **Pandas**: Data manipulation and analysis ([Pandas Documentation](https://pandas.pydata.org/))
- **ChromaDB**: Vector database for memory management ([ChromaDB Documentation](https://docs.trychroma.com/))
- **HuggingFace**: Open-source provider of NLP technologies ([HuggingFace Documentation](https://huggingface.co/docs))
- **LM Studio**: To download and run local open-source LLMs ([LM Studio](https://lmstudio.ai/))

## 🌟 Key Features
- **LLM-Powered Generative Agents**: Agents dynamically reason and adapt to the environment.
- **RAG-Driven Responses**: Combines powerful retrieval systems with generative models to provide different content recommendations to agents.
- **Memory Mechanisms**: Agents retain and prioritize past interactions.
- **Emergent Social Phenomena**: Agents naturally replicates real-world social phenomena. 

## 📰 Our papers and other useful links

* [Jan 2025] **"Agent-Based Modelling Meets Generative AI in Social Network Simulations"**, [Paper](https://link.springer.com/chapter/10.1007/978-3-031-78541-2_10)
* [Feb 2025] **"Can Generative Agent-Based Modeling Replicate the Friendship Paradox in Social Media Simulations?"**, [Paper](https://arxiv.org/abs/2502.05919)

Check out our [LLM-Agents-For-Simulation](https://github.com/giammy677dev/LLM-Agents-for-Simulation) repository!

## 🙏 Acknowledgments
This project was developed as part of PhD research at the University of Naples Federico II. Special thanks to my supervisor Professor *Vincenzo Moscato* and my co-tutor *Valerio La Gatta* for their invaluable contributions and support.

Please create an issue if something isn't working for you. We'll be happy to help.

## 📜 License

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
