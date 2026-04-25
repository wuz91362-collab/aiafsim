
import json
import time
from urllib import error, request

# 从配置文件获取的默认值
OLLAMA_URL = "http://localhost:11433/api/generate"
MODEL = "hopephoto/qwen3-4b-instruct-2507_q8"
TIMEOUT_SECONDS = 180

def test_ollama_connection():
    """测试Ollama连接和模型是否可用"""
    print(f"正在测试 Ollama 连接...")
    print(f"URL: {OLLAMA_URL}")
    print(f"模型: {MODEL}")
    print(f"超时: {TIMEOUT_SECONDS}秒")
    print("-" * 50)

    # 准备测试请求
    payload = {
        "model": MODEL,
        "prompt": "你好,你可以写100字的小作文吗。",
        "stream": False,
        "options": {"temperature": 1},
    }

    req = request.Request(
        url=OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        print("发送测试请求...")
        start_time = time.time()
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            end_time = time.time()
            response_time = end_time - start_time

            body = json.loads(resp.read().decode("utf-8"))
            response = body.get("response", "").strip()

            if response:
                print("✓ Ollama 连接成功!")
                print("✓ 模型响应正常!")
                print(f"✓ 模型回复时间: {response_time:.2f}秒")
                print("-" * 50)
                print("模型回复:")
                print(response)
                return True
            else:
                print("✗ Ollama 返回空响应")
                return False

    except error.URLError as exc:
        print(f"✗ 连接失败: {exc}")
        print("\n请确保:")
        print("1. Ollama 服务已启动")
        print("2. 模型已下载: ollama pull hopephoto/qwen3-4b-thinking-2507_q8")
        print("3. Ollama 运行在默认端口 11434")
        return False

    except TimeoutError:
        print("✗ 请求超时")
        print("\n可能原因:")
        print("1. 模型加载时间过长")
        print("2. 系统资源不足")
        return False

    except json.JSONDecodeError:
        print("✗ 响应解析失败")
        return False
    except Exception as exc:
        print(f"✗ 未知错误: {exc}")
        return False

if __name__ == "__main__":
    success = test_ollama_connection()
    print("" + "=" * 50)
    if success:
        print("测试结果: 模型可用 ✓")
    else:
        print("测试结果: 模型不可用 ✗")
    print("=" * 50)
