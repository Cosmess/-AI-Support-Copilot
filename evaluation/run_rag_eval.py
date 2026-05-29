import json
from pathlib import Path
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from support_copilot.application.use_cases.answer_support_question import AnswerSupportQuestion
from support_copilot.infrastructure.adapters.fallbacks import NullLogProvider, NullTicketProvider
from support_copilot.infrastructure.adapters.kb_chroma import ChromaKnowledgeRepository
from support_copilot.infrastructure.adapters.llm_openai import OpenAILLMProvider


def main() -> None:
    kb = ChromaKnowledgeRepository()
    llm = OpenAILLMProvider()
    use_case = AnswerSupportQuestion(kb=kb, tickets=NullTicketProvider(), logs=NullLogProvider(), llm=llm)

    rows = []
    dataset_path = Path("evaluation/rag_eval_dataset.jsonl")
    for line in dataset_path.read_text(encoding="utf-8").splitlines():
        sample = json.loads(line)
        output = use_case.execute(sample["question"])
        rows.append(
            {
                "question": sample["question"],
                "answer": output["answer"]["raw_response"],
                "contexts": output["retrieved_context"],
                "ground_truth": sample["ground_truth"],
            }
        )

    ds = Dataset.from_list(rows)
    result = evaluate(ds, metrics=[faithfulness, answer_relevancy, context_precision])
    print(result)


if __name__ == "__main__":
    main()
