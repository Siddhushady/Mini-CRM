# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from models import db, Lead
import os
import random

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mini_crm.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'devkey-change-me'  # for flash messages; replace in prod

    db.init_app(app)

    @app.route('/')
    def index():
        # Dashboard summary: counts by status
        status_counts = {}
        statuses = ['new', 'contacted', 'qualified', 'converted', 'lost']
        for s in statuses:
            status_counts[s] = Lead.query.filter_by(status=s).count()

        total_leads = Lead.query.count()

        # Top 5 leads by score
        top_leads = Lead.query.order_by(Lead.score.desc()).limit(5).all()

        return render_template(
            'index.html',
            status_counts=status_counts,
            total_leads=total_leads,
            top_leads=top_leads
        )


    @app.route('/leads')
    def view_leads():
        status = request.args.get('status')
        if status:
            leads = Lead.query.filter_by(status=status).order_by(Lead.created_at.desc()).all()
        else:
            leads = Lead.query.order_by(Lead.created_at.desc()).all()
        return render_template('view_leads.html', leads=leads)

    @app.route('/lead/<int:lead_id>')
    def lead_detail(lead_id):
        lead = Lead.query.get_or_404(lead_id)
        return render_template('lead_detail.html', lead=lead)

    @app.route('/lead/add', methods=['GET', 'POST'])
    def add_lead():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            source = request.form.get('source') or 'website'
            notes = request.form.get('notes')
            # simple score heuristic: random for demo; in real app compute based on fields
            score = int(request.form.get('score') or random.randint(10, 90))
            lead = Lead(name=name, email=email, phone=phone, source=source, notes=notes, score=score)
            db.session.add(lead)
            db.session.commit()
            flash('Lead added successfully', 'success')
            return redirect(url_for('view_leads'))
        return render_template('add_lead.html')

    @app.route('/lead/<int:lead_id>/update', methods=['POST'])
    def update_lead(lead_id):
        lead = Lead.query.get_or_404(lead_id)
        lead.name = request.form.get('name') or lead.name
        lead.email = request.form.get('email') or lead.email
        lead.phone = request.form.get('phone') or lead.phone
        lead.source = request.form.get('source') or lead.source
        lead.status = request.form.get('status') or lead.status
        lead.score = int(request.form.get('score') or lead.score)
        lead.notes = request.form.get('notes') or lead.notes
        db.session.commit()
        flash('Lead updated', 'info')
        return redirect(url_for('lead_detail', lead_id=lead.id))

    @app.route('/api/leads', methods=['GET', 'POST'])
    def api_leads():
        if request.method == 'GET':
            leads = Lead.query.order_by(Lead.created_at.desc()).all()
            return jsonify([l.to_dict() for l in leads])
        else:
            data = request.get_json() or {}
            name = data.get('name')
            if not name:
                return jsonify({'error': 'name required'}), 400
            lead = Lead(
                name=name,
                email=data.get('email'),
                phone=data.get('phone'),
                source=data.get('source', 'api'),
                score=int(data.get('score', random.randint(0, 90)))
            )
            db.session.add(lead)
            db.session.commit()
            return jsonify({'status': 'ok', 'lead': lead.to_dict()}), 201

    @app.route('/automation/run', methods=['POST'])
    def run_automation():
        """
        Simulate simple lead automation rules:
        - If score >= 80 -> qualified
        - If score >= 90 -> converted
        - If email present and not contacted -> set to contacted
        Returns summary JSON. This endpoint can be called manually, by Jenkins, or scheduled.
        """
        leads = Lead.query.filter(Lead.status.in_(['new', 'contacted', 'qualified'])).all()
        processed = {'converted': 0, 'qualified': 0, 'contacted': 0}
        for lead in leads:
            if lead.score >= 90:
                lead.status = 'converted'
                processed['converted'] += 1
            elif lead.score >= 80:
                if lead.status != 'qualified':
                    lead.status = 'qualified'
                    processed['qualified'] += 1
            elif lead.email and lead.status == 'new':
                lead.status = 'contacted'
                processed['contacted'] += 1
        db.session.commit()
        return jsonify({'status': 'ok', 'processed': processed})

    @app.route('/api/automation/preview', methods=['GET'])
    def automation_preview():
        """
        Return which leads would be changed by automation without applying changes.
        """
        leads = Lead.query.filter(Lead.status.in_(['new', 'contacted', 'qualified'])).all()
        transforms = []
        for lead in leads:
            new_status = lead.status
            if lead.score >= 90:
                new_status = 'converted'
            elif lead.score >= 80:
                new_status = 'qualified'
            elif lead.email and lead.status == 'new':
                new_status = 'contacted'
            if new_status != lead.status:
                transforms.append({'id': lead.id, 'from': lead.status, 'to': new_status, 'score': lead.score})
        return jsonify(transforms)

    return app

if __name__ == '__main__':
    app = create_app()
    # ensure DB exists
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
