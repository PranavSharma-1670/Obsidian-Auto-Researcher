# 1. Open Source Toolkits For LLM Development and Deployment

There are various frameworks and libraries developed for LLM training, evaluation, and deployment, and covering every single framework is out of this paper’s scope. But we try to provide a brief introduction of some of the most popular ones, grouped into different categories.

## A. LLM Training/Inference Frameworks

Some of the popular frameworks which are useful for LLM training includes (note that some of them can be used beyond LLM training too):

**DeepSpeed [221]** is a deep learning optimization library that makes distributed training and inference easy, efficient, and effective. DeepSpeed enables world’s most powerful language models like MT-530B and BLOOM. It is an easy-to-use deep learning optimization software suite that powers unprecedented scale and speed for both training and inference. With DeepSpeed you can:

**Transformers [222]** is library by HuggingFace which provides thousands of pretrained models to perform tasks on different modalities such as text, vision, and audio. Using pretrained models one can reduce compute costs, carbon footprint, and save the time and resources required to train a model from scratch.

**Megatron-LM [223]** is a large, powerful transformer developed by the Applied Deep Learning Research team at NVIDIA. It contains efficient, model-parallel (tensor, sequence, and pipeline), and multi-node pre-training of transformer based models such as GPT, BERT, and T5 using mixed precision.

**BMTrain [224]** is an efficient large model training toolkit that can be used to train large models with tens of billions of parameters. It can train models in a distributed manner while keeping the code as simple as stand-alone training.

**GPT-NeoX [225]** leverages many of the same features and technologies as the popular Megatron-DeepSpeed library but with substantially increased usability and novel optimizations.

**LoRA [226]** library provides the support for Low-Rank Adaptation of Large Language Models. It reduces the number of trainable parameters by learning pairs of rank-decompostion matrices while freezing the original weights. This vastly reduces the storage requirement for large language models adapted to specific tasks and enables efficient task-switching during deployment all without introducing inference latency. LoRA also outperforms several other adaptation methods including adapter, prefix-tuning, and fine-tuning.

**ColossalAI library [227]** provides a collection of parallel components. It aims to support developers to write their distributed deep learning models just like how they write their model on their laptop. They provide user-friendly tools to kickstart distributed training and inference in a few lines. In terms of Parallelism strategies, they support: Data Parallelism, Pipeline Parallelism, Sequence Parallelism, Zero Redundancy Optimizer (ZeRO) [140], and Auto-Parallelism.

## B. Deployment Tools

We provide an overview of some of the most popular LLM deployment tools here.

**FastChat [228]** is an open platform for training, serving, and evaluating large language model based chatbots. FastChat’s core features include: The training and evaluation code for state-of-the-art models (e.g., Vicuna, MT-Bench), and a distributed multi-model serving system with web UI and OpenAI-compatible RESTful APIs.

**Skypilot [229]** is a framework for running LLMs, AI, and batch jobs on any cloud, offering maximum cost savings, highest GPU availability, and managed execution.

**vLLM [230]** is a fast and easy-to-use library for LLM inference and serving. vLLM seamlessly supports many Hugging Face models, including the following architectures: Aquila, Baichuan, BLOOM, ChatGLM, DeciLM, Falcon, GPT Big-Code, LLaMA, LLaMA 2, Mistral, Mixtral, MPT, OPT, Qwen, Yi, and many more.

**text-generation-inference [231]** is a toolkit for deploying and serving Large Language Models (LLMs). TGI enables high-performance text generation for the most popular open-source LLMs, including Llama, Falcon, StarCoder, BLOOM, GPT-NeoX, and more.

**LangChain [232]** is a framework for developing applications powered by language models. It enables applications that:
- Are context-aware: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)
- Reason: rely on a language model to reason (about how to answer based on provided context, what actions to take, etc.)

**OpenLLM [233]** is an open-source platform designed to facilitate the deployment and operation of large language models (LLMs) in real-world applications. With OpenLLM, you can run inference on any open-source LLM, deploy them on the cloud or on-premises, and build powerful AI applications.

**Embedchain [234]** is an Open Source RAG Framework that makes it easy to create and deploy AI apps. Embedchain streamlines the creation of RAG applications, offering a seamless process for managing various types of unstructured data. It efficiently segments data into manageable chunks, generates relevant embeddings, and stores them in a vector database for optimized retrieval.

**Autogen [235]** is a framework that enables the development of LLM applications using multiple agents that can converse with each other to solve tasks. AutoGen agents are customizable, conversable, and seamlessly allow human participation. They can operate in various modes that employ combinations of LLMs, human inputs, and tools.

**BabyAGI [236]** is an autonomous Artificial Intelligence agent, that is designed to generate and execute tasks based on given objectives. It harnesses cutting-edge technologies from OpenAI, Pinecone, LangChain, and Chroma to automate tasks and achieve specific goals. In this blog post, we will dive into the unique features of BabyAGI and explore how it can streamline task automation.

## C. Prompting Libraries

**Guidance [237]** is a programming paradigm that offers superior control and efficiency compared to conventional prompting and chaining. It allows users to constrain generation (e.g. with regex and CFGs) as well as to interleave control (conditional, loops) and generation seamlessly.

**PromptTools [238]** offers a set of open-source, self-hostable tools for experimenting with, testing, and evaluating LLMs, vector databases, and prompts. The core idea is to enable developers to evaluate using familiar interfaces like code, notebooks, and a local playground.

**PromptBench [?]** is a Pytorch-based Python package for Evaluation of Large Language Models (LLMs). It provides user-friendly APIs for researchers to conduct evaluation on LLMs.

**Promptfoo [239]** is a tool for testing and evaluating LLM output quality. It systematically test prompts, models, and RAGs with predefined test cases.

## D. VectorDB

**Faiss [240]** is a library developed by Facebook AI Research that provides efficient similarity search and clustering of dense vectors. It is designed for use with large-scale, high-dimensional data and supports several index types and algorithms for various use cases.

**Milvus [241]** is an open-source vector database built to power embedding similarity search and AI applications. Milvus makes unstructured data search more accessible, and provides a consistent user experience regardless of the deployment environment.

**Qdrant [242]** is a vector similarity search engine and vector database. It provides a production-ready service with a convenient API to store, search, and manage points—vectors with an additional payload Qdrant is tailored to extended filtering support. environment.

**Weaviate [243]** is an open-source, GraphQL-based vector search engine that enables similarity search on high-dimensional data. While it is open-source, the commercial version offers additional features, support, and managed services.

Some of the other popular options includes LlamaIndex [244] and Pinecone.