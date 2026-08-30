import os
import shutil
import sys
from pathlib import Path

from django.conf import settings

PROJECT_ROOT = settings.BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.baseline import StatisticalForecastBaseline  # noqa: E402


def get_baseline() -> StatisticalForecastBaseline:
    dataset_root = Path(os.getenv("VISUELLE2_ROOT", PROJECT_ROOT / "visuelle2"))
    if not dataset_root.is_absolute():
        dataset_root = PROJECT_ROOT / dataset_root
    return StatisticalForecastBaseline(dataset_root.resolve())


def attach_dataset_image(design) -> str:
    source = get_baseline().match_image(design.category, design.color, design.fabric)
    target_dir = settings.MEDIA_ROOT / "designs"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{design.pk}-{source.name}"
    shutil.copy2(source, target)
    design.image_path = f"{settings.MEDIA_URL}designs/{target.name}"
    design.image_source = "visuelle2-match"
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

