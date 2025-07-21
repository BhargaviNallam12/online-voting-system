from app import app, db, Candidate

with app.app_context():
    db.create_all()  # Ensure tables exist

    # Add candidates
    candidates = ["Alice", "Bob", "Charlie"]
    for name in candidates:
        if not Candidate.query.filter_by(name=name).first():
            db.session.add(Candidate(name=name))

    db.session.commit()
    print("✅ Candidates added successfully!")
