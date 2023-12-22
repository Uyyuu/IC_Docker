from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースの格納先
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'

# crud操作を行う上での基盤の設定
engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={'check_same_thread': False}
            # check_same_threadはDBがsqliteの時のみ必要な引数
        )

# セッションの定義
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# データベースの構造などを定義する際に継承するクラスのようなもの
Base = declarative_base()