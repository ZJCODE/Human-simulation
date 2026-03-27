# 项目点评 / Project Review

## 项目概述 / Overview

**Human-simulation** 是一个基于位置匹配和观点匹配的人类社交行为仿真项目，核心思想是模拟"志同道合"——人与人之间因地理位置接近而相遇，并因观点相似而成为朋友。

> **Human-simulation** is a social interaction simulation based on location proximity and opinion similarity — modeling how people meet and bond ("birds of a feather flock together").

---

## 亮点 / Strengths

1. **概念清晰，富有创意**：用简洁的数学模型（物理位置 + 观点向量）来模拟人类社交网络的形成，立意新颖，具有一定的学术价值。

2. **高效采样算法**：`utils.py` 中实现了 [Alias Method（别名采样法）](https://en.wikipedia.org/wiki/Alias_method)，时间复杂度 O(1)，避免了朴素采样的低效，体现了良好的算法素养。

3. **可视化支持**：利用 `matplotlib` 对每个 human 的运动轨迹进行绘制，直观展现仿真结果（见 `Result/` 目录中的截图）。

4. **参数化设计**：`walk_random_level`、`opinion_agree_level`、`opinion_influence_level` 等参数均可配置，方便进行不同场景的实验。

---

## 问题与改进建议 / Issues & Improvement Suggestions

### 1. `environment.py` 实际为空 / `environment.py` is essentially empty

```python
class environment:
    def __init__(self):
        pass
```

`environment.py` 中的 `environment` 类没有任何实现，而 `human.py` 的 `__main__` 里甚至有注释 `# move this to environment`，说明这部分工作尚未完成。建议将全局仿真循环（人员初始化、时间步推进、可视化）迁移到 `environment` 类中。

---

### 2. `np.int` 已弃用 / `np.int` is deprecated

```python
# utils.py line 17
J = np.zeros(K, dtype=np.int)  # 已在 NumPy 1.20+ 中弃用，1.24 中移除
```

应改为：

```python
J = np.zeros(K, dtype=int)
```

---

### 3. `_opinion_influence` 存在顺序依赖缺陷 / Asymmetric update bug in `_opinion_influence`

```python
def _opinion_influence(self, someone, opinion_influence_level):
    self.opinion = self.opinion + opinion_influence_level * someone.opinion   # self 先更新
    someone.opinion = someone.opinion + opinion_influence_level * self.opinion  # 此时用的是已更新的 self.opinion!
```

第二行使用的是**已经更新过**的 `self.opinion`，导致两者的影响不对称。应先保存原始值：

```python
def _opinion_influence(self, someone, opinion_influence_level):
    self_opinion_orig = self.opinion.copy()
    self.opinion = self.opinion + opinion_influence_level * someone.opinion
    someone.opinion = someone.opinion + opinion_influence_level * self_opinion_orig
```

---

### 4. 大量 `print` 语句影响性能 / Excessive `print` calls hurt performance

仿真循环中每次相遇、对话都会调用 `print`，在 30 个 human × 300 个时间步的场景下，会产生数十万行输出，严重拖慢运行速度。建议用 Python 标准库 `logging` 替代，并通过日志级别控制输出详细程度：

```python
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# 用 logger.debug(...) 替换 print(...)
```

---

### 5. 重复维护两套字典 / Duplicate identity and object dictionaries

每个 human 同时维护了：

- `human_meet_set`（以 identity 字符串为键）
- `human_meet_set_obj`（以 human 对象为键）

以及类似的 `human_opinion_match_set` / `human_opinion_match_set_obj`。这导致同一份数据存储了两次，且每次更新都需要同步两个字典，容易产生不一致。建议统一使用对象引用作为键，通过 `someone.identity` 属性获取名称：

```python
# 只保留一个字典
self.human_meet_set = {}  # key: human object, value: count
```

---

### 6. `opinion_match` 只有单向交流 / One-sided conversation in `opinion_match`

目前的对话逻辑是 `self` 说话，`someone` 回应。`someone` 从不主动表达自己的观点，导致社交关系的建立完全是单向驱动的。可以让双方都发言，使匹配更加对称。

---

### 7. 颜色生成器被消费两次 / Color generator consumed twice per human

```python
color_generator = utils.get_color()
for h in humans:
    h.plot_location_trace(next(color_generator))          # 消费一次
    plt.plot(..., '{}.'.format(next(color_generator)), ...)  # 又消费一次
```

同一个 human 的轨迹线和终点标记会使用**不同的颜色**，应使用同一颜色：

```python
color_generator = utils.get_color()
for h in humans:
    color = next(color_generator)
    h.plot_location_trace(color)
    plt.plot(..., '{}.'.format(color), ...)
```

---

### 8. 缺少测试与文档 / No tests or docstrings

项目缺少单元测试和函数文档字符串，建议：

- 为 `utils.py` 中的 `alias_setup`、`alias_draw`、`softmax` 添加 docstring 和单元测试；
- 为 `human` 类的核心方法添加 docstring，说明参数含义和返回值；
- 使用 `pytest` 搭建基本测试框架。

---

### 9. `human.py` 职责混杂 / `human.py` mixes class definition with simulation entry point

建议将 `if __name__ == '__main__':` 块内的仿真逻辑移至独立的 `main.py` 或 `simulate.py`，保持 `human.py` 只负责定义 `human` 类，遵循单一职责原则。

---

## 总结 / Summary

| 维度 | 评价 |
|------|------|
| 创意与立意 | ⭐⭐⭐⭐⭐ |
| 代码可读性 | ⭐⭐⭐ |
| 算法质量 | ⭐⭐⭐⭐ |
| 代码健壮性 | ⭐⭐ |
| 测试覆盖率 | ⭐ |
| 完成度 | ⭐⭐⭐ |

整体而言，这是一个思路有趣、有一定技术深度的小型仿真项目。核心算法（Alias 采样、softmax 观点表达、随机游走）实现得较为扎实，但工程完成度有待提高——`environment.py` 未实现、存在 API 弃用警告、逻辑缺陷（`_opinion_influence`）以及性能隐患（大量 print）等问题需要修复，同时建议补充测试和文档以提升项目质量。
