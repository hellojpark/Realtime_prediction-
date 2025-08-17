"""
Streamlit 앱 실행 스크립트
"""

import subprocess
import sys
import os
from pathlib import Path


def check_requirements():
    """필요한 패키지들이 설치되어 있는지 확인"""
    
    # 패키지 이름과 import 이름이 다른 경우 매핑
    package_mapping = {
        'streamlit': 'streamlit',
        'langchain': 'langchain', 
        'openai': 'openai',
        'faiss-cpu': 'faiss',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    
    for package_name, import_name in package_mapping.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ 다음 패키지들이 설치되어 있지 않습니다:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n다음 명령어로 설치해주세요:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True


def check_openai_key():
    """OpenAI API 키 확인"""
    
    # 프로젝트 루트의 .env 파일 확인
    try:
        from dotenv import load_dotenv
        project_root = Path(__file__).parent.parent
        env_path = project_root / ".env"
        load_dotenv(dotenv_path=env_path, override=False)
    except ImportError:
        pass
    
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        env_path = Path(__file__).parent.parent / ".env"
        print("⚠️  OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("\n💡 다음 중 하나의 방법으로 설정해주세요:")
        print("   1. 시스템 환경변수로 설정")
        print("   2. 터미널에서: set OPENAI_API_KEY=your_key_here (Windows)")
        print("   3. 터미널에서: export OPENAI_API_KEY=your_key_here (Mac/Linux)")
        print(f"   4. {env_path} 파일에서 OPENAI_API_KEY=your_key_here 설정")
        print("\n🔑 OpenAI API 키는 https://platform.openai.com/api-keys 에서 발급받으세요.")
        return False
    
    return True


def setup_rag_system():
    """RAG 시스템 백그라운드 설정"""
    print("\n📦 RAG 시스템 사전 준비 중...")
    
    try:
        # RAG 모듈 경로 추가
        rag_path = Path(__file__).parent.parent / "rag"
        sys.path.insert(0, str(rag_path))
        
        from rag_system import EstateRAGSystem
        from vector_store import VectorStoreManager
        
        # 벡터스토어 캐시 확인
        vm = VectorStoreManager()
        cache_info = vm.get_cache_info()
        
        if cache_info.get("exists", False):
            print(f"✅ 기존 벡터스토어 캐시 발견 ({cache_info.get('size_mb', 'N/A')} MB)")
            print("🚀 빠른 시작이 가능합니다!")
        else:
            print("⚠️  벡터스토어 캐시가 없습니다.")
            print("💡 첫 실행 시 1-2분의 초기화 시간이 필요합니다.")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  RAG 모듈 로드 실패: {e}")
        print("💡 앱에서 수동으로 초기화하세요.")
        return False
    except Exception as e:
        print(f"⚠️  RAG 시스템 확인 중 오류: {e}")
        return False


def main():
    """메인 실행 함수"""
    
    print("🏠 AI 부동산 분석 플랫폼을 시작합니다...")
    print("=" * 60)
    
    # 1. 패키지 확인
    print("1. 필요 패키지 확인 중...")
    if not check_requirements():
        sys.exit(1)
    
    # 2. OpenAI API 키 확인
    print("\n2. OpenAI API 키 확인 중...")
    if not check_openai_key():
        print("💡 환경변수 설정 후 다시 실행해주세요.")
        sys.exit(1)
    
    # 3. RAG 시스템 사전 체크
    print("\n3. RAG 시스템 사전 체크 중...")
    setup_rag_system()
    
    # 4. Streamlit 앱 실행
    print("\n4. 웹 애플리케이션을 시작합니다...")
    print("🌐 브라우저에서 http://localhost:8501 로 접속하세요.")
    print("📱 모바일에서도 접속 가능합니다!")
    print("⚠️  앱을 종료하려면 Ctrl+C를 누르세요.")
    print("\n💡 실행 방법:")
    print("   - 권장: python run_app.py (사전 체크 포함)")
    print("   - 직접: streamlit run app.py (사전 체크 없음)")
    print("=" * 60)
    
    try:
        # Streamlit 실행
        app_path = Path(__file__).parent / "app.py"
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.address", "localhost",
            "--server.port", "8501",
            "--server.headless", "false"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 AI 부동산 분석 플랫폼이 종료되었습니다.")
        print("💾 모든 데이터와 캐시는 안전하게 보존됩니다.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()