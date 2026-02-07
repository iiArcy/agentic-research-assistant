from huggingface_hub import HfApi

from config.settings import settings


def search_huggingface(query: str) -> list[dict]:
    """Search HuggingFace Hub for models matching the query.

    Returns a list of Citation dicts with source_type="huggingface".
    """
    token = settings.huggingface_token or None
    api = HfApi(token=token)

    citations = []
    try:
        models = api.list_models(
            search=query,
            sort="downloads",
            limit=settings.huggingface_max_results,
        )
        for model in models:
            model_id = model.id
            pipeline_tag = model.pipeline_tag or "unknown"
            downloads = model.downloads or 0
            likes = model.likes or 0
            tags = model.tags or []

            tag_str = ", ".join(tags[:5])
            snippet = (
                f"{pipeline_tag} model — {downloads:,} downloads, {likes} likes. "
                f"Tags: {tag_str}"
            )

            citations.append({
                "source_type": "huggingface",
                "title": model_id,
                "url": f"https://huggingface.co/{model_id}",
                "snippet": snippet,
            })
    except Exception:
        pass

    return citations
