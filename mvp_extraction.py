import spacy
import json

# 1. 初始化：加载 spaCy 的轻量级英文模型
# 该模型负责句法分析，能够识别词性以及词与词之间的依存关系
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("请先运行: python -m spacy download en_core_web_sm")
    exit()

# 2. 输入部分：使用占位符防止数据污染
# 你可以在实际运行时将 "xxxxx" 替换为需要测试的句子.
text = "xxxxx" 

# 处理文本，生成 spaCy 的 Doc 对象（包含词法和句法分析结果）
doc = nlp(text)

# 3. 专项识别子模块逻辑（属性提取）
# 我们创建一个字典来存储提取到的实体及其属性
# 结构：{ "实体名称": {"属性类型": "属性值"} }
extracted_data = {}

print(f"正在分析文本: {text}")

for token in doc:
    # 【关键逻辑】：检查 token 是否为 'amod' (Adjectival Modifier)
    # amod 表示该词是一个形容词，且正在修饰它的 head（中心词/名词）
    # 这实现了“属性”与“实体”的精准绑定，而非简单的关键词匹配
    if token.dep_ == "amod":
        attribute_value = token.text      # 提取属性值（例如：red, blue）
        entity_name = token.head.text     # 提取被修饰的实体（例如：circle, square）
        
        # 为了 MVP 简单起见，我们将属性直接记录在实体下
        # 在实际复杂场景中，这里可以进一步判断 attribute_value 是否属于颜色或形状类
        if entity_name not in extracted_data:
            extracted_data[entity_name] = {}
        
        # 将属性挂载到实体上
        extracted_data[entity_name]["attribute"] = attribute_value
        print(f"识别到绑定关系: [{attribute_value}] -> [{entity_name}]")

# 4. 属性挂载 (JSON 记忆空间)
# 将提取到的结构化数据持久化到本地 JSON 文件中
memory_file = "memory.json"

try:
    with open(memory_file, "w", encoding="utf-8") as f:
        # indent=4 使 JSON 文件具有可读性，方便人工核查（白盒化）
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)
    print(f"\n属性已成功挂载至记忆空间: {memory_file}")
except Exception as e:
    print(f"写入记忆空间时出错: {e}")

# 最终结果展示
print("\n--- 当前记忆状态 ---")
print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
