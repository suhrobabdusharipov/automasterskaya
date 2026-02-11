from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import date, datetime, timedelta
import tempfile
import os
from typing import Optional

from backend.database import get_db
from backend.models.order import Order
from backend.models.contract import Contract
from backend.models.client import Client
from backend.models.car import Car
from backend.models.service import Service
from backend.models.spare_part import SparePart

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/")
def reports_page(request: Request):
    return templates.TemplateResponse(
        "reports/index.html",
        {"request": request}
    )

@router.get("/orders")
def orders_report_page(request: Request):
    return templates.TemplateResponse(
        "reports/orders.html",
        {
            "request": request,
            "today": date.today().strftime("%Y-%m-%d"),
            "week_ago": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        }
    )

@router.get("/financial")
def financial_report_page(request: Request):
    return templates.TemplateResponse(
        "reports/financial.html",
        {
            "request": request,
            "today": date.today().strftime("%Y-%m-%d"),
            "month_start": date.today().replace(day=1).strftime("%Y-%m-%d")
        }
    )

@router.get("/clients")
def clients_report_page(request: Request):
    return templates.TemplateResponse(
        "reports/clients.html",
        {"request": request}
    )

@router.get("/services")
def services_report_page(request: Request):
    return templates.TemplateResponse(
        "reports/services.html",
        {"request": request}
    )

@router.get("/spare-parts")
def spare_parts_report_page(request: Request):
    return templates.TemplateResponse(
        "reports/spare_parts.html",
        {"request": request}
    )

@router.get("/api/orders")
def get_orders_report(
    db: Session = Depends(get_db),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    query = db.query(
        Order.id,
        Order.date,
        Order.total_cost,
        Order.services_description,
        Contract.id.label('contract_id'),
        Client.full_name.label('client_name'),
        Car.brand,
        Car.model,
        Car.vin
    ).join(
        Contract, Order.contract_id == Contract.id
    ).join(
        Client, Contract.client_id == Client.id
    ).join(
        Car, Contract.car_id == Car.id
    )
    
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Order.date >= start)
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Order.date < end)
    
    if status:
        query = query.filter(Contract.status == status)
    
    orders = query.order_by(desc(Order.date)).all()
    
    total_orders = len(orders)
    total_revenue = sum(order.total_cost or 0 for order in orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    return {
        "orders": [
            {
                "id": o.id,
                "date": o.date,
                "total_cost": float(o.total_cost or 0),
                "description": o.services_description,
                "contract_id": o.contract_id,
                "client_name": o.client_name,
                "car": f"{o.brand} {o.model}",
                "vin": o.vin
            }
            for o in orders
        ],
        "summary": {
            "total_orders": total_orders,
            "total_revenue": float(total_revenue),
            "avg_order_value": float(avg_order_value)
        }
    }

@router.get("/api/financial")
def get_financial_report(
    db: Session = Depends(get_db),
    period: str = Query("month"),  
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    else:
        end = datetime.now()
        if period == "day":
            start = end - timedelta(days=1)
        elif period == "week":
            start = end - timedelta(days=7)
        elif period == "month":
            start = end - timedelta(days=30)
        elif period == "quarter":
            start = end - timedelta(days=90)
        elif period == "year":
            start = end - timedelta(days=365)
        else:
            start = end - timedelta(days=30)
    
    orders = db.query(Order).filter(
        and_(Order.date >= start, Order.date < end)
    ).all()
    
    revenue_by_day = {}
    for order in orders:
        day = order.date.strftime("%Y-%m-%d")
        revenue_by_day[day] = revenue_by_day.get(day, 0) + (order.total_cost or 0)
    
    status_stats = db.query(
        Contract.status,
        func.count(Contract.id).label('count'),
        func.sum(Contract.total_amount).label('total')
    ).filter(
        and_(Contract.date >= start.date(), Contract.date < end.date())
    ).group_by(Contract.status).all()
    
    top_services = [
        {"name": "Замена масла", "count": 15, "revenue": 75000},
        {"name": "Диагностика", "count": 12, "revenue": 36000},
        {"name": "Шиномонтаж", "count": 10, "revenue": 25000}
    ]
    
    top_parts = [
        {"name": "Масло моторное", "quantity": 25, "revenue": 37500},
        {"name": "Фильтр масляный", "quantity": 20, "revenue": 8000},
        {"name": "Тормозные колодки", "quantity": 15, "revenue": 22500}
    ]
    
    return {
        "period": {
            "start": start.strftime("%Y-%m-%d"),
            "end": (end - timedelta(days=1)).strftime("%Y-%m-%d")
        },
        "summary": {
            "total_orders": len(orders),
            "total_revenue": float(sum(o.total_cost or 0 for o in orders)),
            "avg_order": float(sum(o.total_cost or 0 for o in orders) / len(orders)) if orders else 0
        },
        "revenue_by_day": [
            {"date": d, "revenue": float(v)} 
            for d, v in sorted(revenue_by_day.items())
        ],
        "status_stats": [
            {
                "status": s.status,
                "count": s.count,
                "total": float(s.total or 0)
            }
            for s in status_stats
        ],
        "top_services": top_services,
        "top_parts": top_parts
    }

@router.get("/api/clients")
def get_clients_report(db: Session = Depends(get_db)):
    top_clients = db.query(
        Client.id,
        Client.full_name,
        Client.phone,
        Client.email,
        func.count(Order.id).label('orders_count'),
        func.sum(Order.total_cost).label('total_spent')
    ).join(
        Contract, Client.id == Contract.client_id
    ).join(
        Order, Contract.id == Order.contract_id
    ).group_by(
        Client.id
    ).order_by(
        desc(func.sum(Order.total_cost))
    ).limit(10).all()
    
    month_ago = datetime.now() - timedelta(days=30)
    active_clients_count = db.query(Client).join(
        Contract, Client.id == Contract.client_id
    ).join(
        Order, Contract.id == Order.contract_id
    ).filter(
        Order.date >= month_ago
    ).distinct().count()
    
    total_clients = db.query(Client).count()
    
    clients_with_cars = db.query(Client).join(
        Car, Client.id == Car.client_id
    ).distinct().count()
    
    return {
        "summary": {
            "total_clients": total_clients,
            "active_clients": active_clients_count,
            "clients_with_cars": clients_with_cars,
            "inactive_clients": total_clients - active_clients_count
        },
        "top_clients": [
            {
                "id": c.id,
                "full_name": c.full_name,
                "phone": c.phone,
                "email": c.email,
                "orders_count": c.orders_count,
                "total_spent": float(c.total_spent or 0)
            }
            for c in top_clients
        ]
    }

@router.get("/api/services")
def get_services_report(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    
    services_stats = [
        {
            "id": s.id,
            "name": s.name,
            "price": float(s.price),
            "orders_count": 5,
            "total_revenue": float(s.price * 5)
        }
        for s in services
    ]
    
    popular_services = sorted(services_stats, key=lambda x: x['orders_count'], reverse=True)[:5]
    
    return {
        "total_services": len(services),
        "services": services_stats,
        "popular_services": popular_services
    }

@router.get("/api/spare-parts")
def get_spare_parts_report(db: Session = Depends(get_db)):
    parts = db.query(SparePart).all()
    
    low_stock = [p for p in parts if p.quantity < 10]
    
    parts_stats = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "quantity": p.quantity,
            "total_value": float(p.price * p.quantity)
        }
        for p in parts
    ]
    
    low_stock_stats = sorted(
        [p for p in parts_stats if p['quantity'] < 10],
        key=lambda x: x['quantity']
    )
    
    total_value = sum(p['total_value'] for p in parts_stats)
    
    return {
        "summary": {
            "total_parts": len(parts),
            "total_value": float(total_value),
            "low_stock_count": len(low_stock),
            "out_of_stock": len([p for p in parts if p.quantity == 0])
        },
        "parts": parts_stats,
        "low_stock": low_stock_stats
    }

@router.get("/api/order/{order_id}/download")
def download_order_report(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w') as tmp:
        tmp.write(f"АКТ ВЫПОЛНЕННЫХ РАБОТ\n")
        tmp.write(f"Заказ-наряд №{order.id}\n")
        tmp.write(f"Дата: {order.date}\n")
        tmp.write(f"Сумма: {order.total_cost} ₽\n")
        tmp.write(f"Описание работ: {order.services_description}\n")
        tmp_path = tmp.name
    
    return FileResponse(
        tmp_path,
        media_type='text/plain',
        filename=f'order_{order_id}_act.txt'
    )

@router.get("/api/export/orders")
def export_orders_report(
    db: Session = Depends(get_db),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    query = db.query(
        Order.id,
        Order.date,
        Order.total_cost,
        Order.services_description,
        Client.full_name,
        Car.brand,
        Car.model,
        Car.vin
    ).join(
        Contract, Order.contract_id == Contract.id
    ).join(
        Client, Contract.client_id == Client.id
    ).join(
        Car, Contract.car_id == Car.id
    )
    
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Order.date >= start)
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Order.date < end)
    
    orders = query.order_by(desc(Order.date)).all()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', encoding='utf-8') as tmp:
        tmp.write("ID;Дата;Клиент;Автомобиль;VIN;Сумма;Описание\n")
        for o in orders:
            tmp.write(f"{o.id};{o.date.strftime('%d.%m.%Y')};{o.full_name};{o.brand} {o.model};{o.vin};{o.total_cost};{o.services_description or ''}\n")
        tmp_path = tmp.name
    
    return FileResponse(
        tmp_path,
        media_type='text/csv',
        filename=f'orders_report_{date.today().strftime("%Y%m%d")}.csv'
    )

@router.get("/api/export/financial")
def export_financial_report(
    db: Session = Depends(get_db),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    orders = db.query(Order).filter(
        and_(Order.date >= start, Order.date < end)
    ).all()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', encoding='utf-8') as tmp:
        tmp.write("Дата;Заказ №;Сумма\n")
        total = 0
        for o in orders:
            tmp.write(f"{o.date.strftime('%d.%m.%Y')};{o.id};{o.total_cost}\n")
            total += o.total_cost or 0
        tmp.write(f"\nИТОГО;;{total}\n")
        tmp_path = tmp.name
    
    return FileResponse(
        tmp_path,
        media_type='text/csv',
        filename=f'financial_report_{start_date}_{end_date}.csv'
    )
