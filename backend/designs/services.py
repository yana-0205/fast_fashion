from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage

PROJECT_ROOT = settings.BASE_DIR.parent

PRODUCT_OPTIONS = {
    "categories": ["long sleeve", "long dress", "miniskirt", "jumpsuit", "culottes", "sleeveless", "short coat", "shirt dress"],
    "colors": ["black", "white", "blue", "red", "grey", "green", "brown", "yellow", "orange", "violet"],
    "fabrics": ["cotton", "linen", "tulle", "velvet", "acrylic", "satin", "lace", "denim", "wool", "silk"],
    "seasons": ["spring-summer", "autumn-winter"],
}


def save_uploaded_design_image(design, uploaded_file) -> str:
    extension = Path(uploaded_file.name).suffix.lower() or ".jpg"
    relative_path = default_storage.save(f"designs/{design.pk}{extension}", uploaded_file)
    design.image_path = f"{settings.MEDIA_URL}{relative_path}"
    design.image_source = "user-upload"
    design.save(update_fields=["image_path", "image_source"])
    return design.image_path


def build_template_insight(design, forecast: dict) -> dict:
    direction = "前高后低" if forecast["weekly_forecast"][0] > forecast["weekly_forecast"][-1] else "后期增长"
    return {
        "color_analysis": f"{design.color} 是该方案的主色，应结合目标渠道的同色商品密度进一步验证差异化。",
        "fabric_analysis": f"{design.fabric} 与 {design.category} 的组合已使用相近历史商品作为预测参照。",
        "season_analysis": f"方案定位为 {design.season}，正式决策前应结合上市地区天气与时间窗口校正。",
        "price_analysis": f"当前定价为 {design.price}，V1 暂不把价格直接解释为因果影响。",
        "summary": f"匹配历史样本显示销量曲线整体呈{direction}，峰值预计出现在第 {forecast['peak_week']} 周。",
        "source": "deterministic-template-v1",
    }
