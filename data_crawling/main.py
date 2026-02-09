from crawler import NaverLandCrawler

def main():
    """메인 실행 함수"""
    try:
        crawler = NaverLandCrawler()
        crawler.run()
    except KeyboardInterrupt:
        print("\n사용자에 의해 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n프로그램 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 