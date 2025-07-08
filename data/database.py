# data/database.py 
import sqlite3
from datetime import datetime
from core.data_models import TradingDecision, RiskAssessment
import aiosqlite

class DatabaseManager:
    def __init__(self, db_path: str = "trading_agents.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de decisões de trading
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                action TEXT,
                quantity INTEGER,
                price REAL,
                confidence REAL,
                reasoning TEXT,
                risk_level TEXT,
                timestamp DATETIME,
                agent_type TEXT
            )
        ''')
        
        # Tabela de avaliações de risco
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                risk_score REAL,
                volatility REAL,
                liquidity_score REAL,
                correlation_risk REAL,
                recommendation TEXT,
                timestamp DATETIME
            )
        ''')
        
        # Tabela de discussões entre agentes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_discussions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                agent_name TEXT,
                message TEXT,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_decision(self, decision: TradingDecision, agent_type: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trading_decisions 
            (symbol, action, quantity, price, confidence, reasoning, risk_level, timestamp, agent_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            decision.symbol, decision.action.value, decision.quantity, decision.price,
            decision.confidence, decision.reasoning, decision.risk_level.value,
            decision.timestamp, agent_type
        ))
        
        conn.commit()
        conn.close()
    
    def save_risk_assessment(self, assessment: RiskAssessment):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO risk_assessments 
            (symbol, risk_score, volatility, liquidity_score, correlation_risk, recommendation, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            assessment.symbol, assessment.risk_score, assessment.volatility,
            assessment.liquidity_score, assessment.correlation_risk,
            assessment.recommendation, assessment.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def save_discussion(self, session_id: str, agent_name: str, message: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO agent_discussions (session_id, agent_name, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (session_id, agent_name, message, datetime.now()))
        
        conn.commit()
        conn.close()

class AsyncDatabaseManager:
    def __init__(self, db_path: str = "trading_agents.db"):
        self.db_path = db_path
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_path)
        await self.init_database()

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def init_database(self):
        async with self.conn.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS trading_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    action TEXT,
                    quantity INTEGER,
                    price REAL,
                    confidence REAL,
                    reasoning TEXT,
                    risk_level TEXT,
                    timestamp DATETIME,
                    agent_type TEXT
                )
            ''')
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS risk_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    risk_score REAL,
                    volatility REAL,
                    liquidity_score REAL,
                    correlation_risk REAL,
                    recommendation TEXT,
                    timestamp DATETIME
                )
            ''')
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_discussions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    agent_name TEXT,
                    message TEXT,
                    timestamp DATETIME
                )
            ''')
        await self.conn.commit()

    async def save_decision(self, decision, agent_type):
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                '''INSERT INTO trading_decisions 
                (symbol, action, quantity, price, confidence, reasoning, risk_level, timestamp, agent_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    decision.symbol, decision.action.value, decision.quantity, decision.price,
                    decision.confidence, decision.reasoning, decision.risk_level.value,
                    decision.timestamp, agent_type
                )
            )
        await self.conn.commit()

    async def save_risk_assessment(self, assessment):
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                '''INSERT INTO risk_assessments 
                (symbol, risk_score, volatility, liquidity_score, correlation_risk, recommendation, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (
                    assessment.symbol, assessment.risk_score, assessment.volatility,
                    assessment.liquidity_score, assessment.correlation_risk,
                    assessment.recommendation, assessment.timestamp
                )
            )
        await self.conn.commit()

    async def save_discussion(self, session_id, agent_name, message):
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                '''INSERT INTO agent_discussions (session_id, agent_name, message, timestamp)
                VALUES (?, ?, ?, ?)''',
                (session_id, agent_name, message, datetime.now())
            )
        await self.conn.commit() 