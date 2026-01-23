from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/home/bhoopender/new/Learning_GEN_AI/Rag/document_loader/books/1.pdf")

docs = loader.load()

# text = """If much is still to discover about how the animal’s brain trains and self-organizes itself in
# order to process so various and so complex information, a number of recent advances in
# “neurobiology” allow already highlighting some of key mechanisms of this marvels
# machine. Among them one can emphasizes brain’s “modular” structure and its “self-
# organizing” capabilities. In fact, if our simple and inappropriate binary technology remains
# too primitive to achieve the processing ability of these marvels mechanisms, a number of
# those highlighted points could already be sources of inspiration for designing new machine
# learning approaches leading to higher levels of artificial systems’ intelligence (Madani, 2007).
# In this chapter, we deal with machine learning based modular approaches which could offer
# powerful solutions to overcome processing difficulties in the aforementioned frame. If the
# machine learning capability provides processing system’s adaptability and offers an
# appealing alternative for fashioning the processing technique adequacy, the modularity may
# result on a substantial reduction of treatment’s complexity. In fact, the modularity issued
# complexity reduction may be obtained from several instances: it may result from
# distribution of computational effort on several modules; it can emerge from cooperative or
# concurrent contribution of several processing modules in handling a same task; it may drop
# from the modules’ complementary contribution (e.g. specialization of a module on treating a
# given task to be performed).
# A number of works dealing with modular computing and issued architectures have been
# proposed since 1990. Most of them associate a set of Artificial Neural Networks (ANN) in a
# modular structure in order to process a complex task by dividing it into several simpler sub-
# tasks. One can mention active learning approaches (Fahlman & Lebiere, 1990), neural
# networks ensemble concept proposed by (Hanibal, 1993), intelligent hybrid systems (Krogh
# & Vedelsby, 1995), Mixture of experts concept proposed by (Bruske & Sommer, 1995) and
# (Sung & Niyogi, 1995) or structures based on dynamic cells (Lang & Witbrock, 1998). In the
# same years, a number of authors proposed multi-modeling concept for nonlinear systems
# modeling, where a set of simple models is used to sculpt a complex behaviour
# (Goonnatilake & Khebbal, 1996), (Mayoubi et al., 1995), (Murray-Smith & Johansen, 1997),
# (Ernst, 1998)) in order to avoid difficulties (modeling complexity). However, it is important
# to remind that the most of proposed works (except those described in the four latest
# references) remain essentially theoretical and if a relatively consequent number of different
# structures have been proposed, a very few of them have been applied to real-world
# dilemmas solution.
# The present chapter focuses those machine learning based modular approaches which take
# advantage either from modules’ independence (multi-agent approach) or from self-
# organizing multi-modeling ("divide and conquer" paradigm). In other words, we will
# expound online and self-organizing approaches which are used when no a priori learning
# information is available. Within this frame, we will present, detail and discuss two
# challenging applicative aspects: the first one dealing with routing optimization in high
# speed communication networks and the other with complex information processing.
# Concerning the network routing optimization problem, we will describe and evaluate an
# adaptive online machine learning based approach, combining multi-agent based modularity
# and neural network based reinforcement learning ((Mellouk, 2007), (Mellouk, 2008b))."""

splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separator=''
)


result = splitter.split_documents(docs)
print(result[1].page_content)