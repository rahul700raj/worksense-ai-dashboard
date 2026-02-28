"""
Employee Attrition Prediction Model Training
Production-ready ML pipeline with preprocessing, training, and evaluation
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

class AttritionPredictor:
    """
    Production-ready Employee Attrition Prediction Model
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.feature_names = None
        self.feature_importance = None
        
    def load_data(self, filepath='ml-model/employee_data.csv'):
        """Load and prepare dataset"""
        print("📊 Loading dataset...")
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} records")
        print(f"   Attrition rate: {df['attrition'].mean():.2%}")
        return df
    
    def preprocess_data(self, df):
        """
        Data preprocessing pipeline:
        - Handle missing values
        - Feature engineering
        - Scaling
        """
        print("\n🔧 Preprocessing data...")
        
        # Drop employee_id (not a feature)
        if 'employee_id' in df.columns:
            df = df.drop('employee_id', axis=1)
        
        # Handle missing values (if any)
        df = df.fillna(df.median())
        
        # Feature engineering
        df['work_life_balance'] = 40 / df['work_hours']  # Inverse of work hours
        df['promotion_performance_ratio'] = df['promotion_gap'] / (df['performance_score'] + 1)
        df['stress_index'] = (df['work_hours'] * df['overtime_frequency']) / 100
        df['satisfaction_performance'] = df['satisfaction_score'] * df['performance_score']
        
        # Separate features and target
        X = df.drop('attrition', axis=1)
        y = df['attrition']
        
        self.feature_names = X.columns.tolist()
        print(f"✅ Created {len(self.feature_names)} features")
        print(f"   Features: {', '.join(self.feature_names)}")
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, val_size=0.1):
        """Split data into train, validation, and test sets"""
        print(f"\n📂 Splitting data (train: {1-test_size-val_size:.0%}, val: {val_size:.0%}, test: {test_size:.0%})...")
        
        # First split: separate test set
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Second split: separate validation set from training
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=42, stratify=y_temp
        )
        
        print(f"✅ Train set: {len(X_train)} samples")
        print(f"   Validation set: {len(X_val)} samples")
        print(f"   Test set: {len(X_test)} samples")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def scale_features(self, X_train, X_val, X_test):
        """Scale features using StandardScaler"""
        print("\n⚖️  Scaling features...")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("✅ Features scaled")
        
        return X_train_scaled, X_val_scaled, X_test_scaled
    
    def train_xgboost(self, X_train, y_train, X_val, y_val):
        """Train XGBoost model with hyperparameter tuning"""
        print("\n🚀 Training XGBoost model...")
        
        # Define parameter grid for tuning
        param_grid = {
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3],
            'n_estimators': [100, 200, 300],
            'min_child_weight': [1, 3, 5],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        }
        
        # Initialize XGBoost
        xgb = XGBClassifier(
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        )
        
        # Grid search with cross-validation
        print("   Performing hyperparameter tuning...")
        grid_search = GridSearchCV(
            xgb, param_grid, cv=3, scoring='f1', n_jobs=-1, verbose=0
        )
        grid_search.fit(X_train, y_train)
        
        # Best model
        self.model = grid_search.best_estimator_
        
        print(f"✅ Best parameters: {grid_search.best_params_}")
        print(f"   Best CV F1 score: {grid_search.best_score_:.4f}")
        
        # Validation performance
        val_pred = self.model.predict(X_val)
        val_accuracy = accuracy_score(y_val, val_pred)
        val_f1 = f1_score(y_val, val_pred)
        
        print(f"   Validation Accuracy: {val_accuracy:.4f}")
        print(f"   Validation F1 Score: {val_f1:.4f}")
        
        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Comprehensive model evaluation"""
        print("\n📈 Evaluating model on test set...")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"\n{'='*50}")
        print(f"📊 MODEL PERFORMANCE METRICS")
        print(f"{'='*50}")
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
        print(f"F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
        print(f"ROC AUC:   {roc_auc:.4f} ({roc_auc*100:.2f}%)")
        print(f"{'='*50}\n")
        
        # Classification report
        print("📋 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['Retained', 'Attrition']))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print("\n🔢 Confusion Matrix:")
        print(f"                Predicted")
        print(f"              Retained  Attrition")
        print(f"Actual Retained    {cm[0][0]:4d}      {cm[0][1]:4d}")
        print(f"       Attrition   {cm[1][0]:4d}      {cm[1][1]:4d}")
        
        # Save confusion matrix plot
        self.plot_confusion_matrix(cm)
        
        # Save ROC curve
        self.plot_roc_curve(y_test, y_pred_proba, roc_auc)
        
        # Save feature importance
        self.plot_feature_importance()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm.tolist()
        }
    
    def plot_confusion_matrix(self, cm):
        """Plot and save confusion matrix"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Retained', 'Attrition'],
                    yticklabels=['Retained', 'Attrition'])
        plt.title('Confusion Matrix - Employee Attrition Prediction', fontsize=14, fontweight='bold')
        plt.ylabel('Actual', fontsize=12)
        plt.xlabel('Predicted', fontsize=12)
        plt.tight_layout()
        plt.savefig('ml-model/confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("✅ Confusion matrix saved: ml-model/confusion_matrix.png")
        plt.close()
    
    def plot_roc_curve(self, y_test, y_pred_proba, roc_auc):
        """Plot and save ROC curve"""
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='#00d4ff', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title('ROC Curve - Employee Attrition Prediction', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('ml-model/roc_curve.png', dpi=300, bbox_inches='tight')
        print("✅ ROC curve saved: ml-model/roc_curve.png")
        plt.close()
    
    def plot_feature_importance(self):
        """Plot and save feature importance"""
        plt.figure(figsize=(10, 6))
        top_features = self.feature_importance.head(10)
        sns.barplot(data=top_features, x='importance', y='feature', palette='viridis')
        plt.title('Top 10 Feature Importance - Attrition Prediction', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.tight_layout()
        plt.savefig('ml-model/feature_importance.png', dpi=300, bbox_inches='tight')
        print("✅ Feature importance saved: ml-model/feature_importance.png")
        plt.close()
        
        print("\n🏆 Top 10 Most Important Features:")
        for idx, row in top_features.iterrows():
            print(f"   {row['feature']:30s} {row['importance']:.4f}")
    
    def save_model(self, filepath='ml-model/attrition_model.pkl'):
        """Save trained model and scaler"""
        print(f"\n💾 Saving model to {filepath}...")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance
        }
        
        joblib.dump(model_data, filepath)
        print(f"✅ Model saved successfully!")
        print(f"   File size: {joblib.os.path.getsize(filepath) / 1024:.2f} KB")
    
    def load_model(self, filepath='ml-model/attrition_model.pkl'):
        """Load trained model"""
        print(f"📂 Loading model from {filepath}...")
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data['feature_importance']
        
        print("✅ Model loaded successfully!")
        return self
    
    def predict(self, features):
        """Make prediction for new data"""
        # Convert to DataFrame if dict
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        
        # Feature engineering (same as training)
        features['work_life_balance'] = 40 / features['work_hours']
        features['promotion_performance_ratio'] = features['promotion_gap'] / (features['performance_score'] + 1)
        features['stress_index'] = (features['work_hours'] * features['overtime_frequency']) / 100
        features['satisfaction_performance'] = features['satisfaction_score'] * features['performance_score']
        
        # Ensure correct feature order
        features = features[self.feature_names]
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            'attrition': int(prediction),
            'attrition_probability': float(probability[1]),
            'retention_probability': float(probability[0])
        }


def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("🚀 EMPLOYEE ATTRITION PREDICTION MODEL TRAINING")
    print("="*60 + "\n")
    
    # Initialize predictor
    predictor = AttritionPredictor()
    
    # Load data
    df = predictor.load_data()
    
    # Preprocess
    X, y = predictor.preprocess_data(df)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = predictor.split_data(X, y)
    
    # Scale features
    X_train_scaled, X_val_scaled, X_test_scaled = predictor.scale_features(
        X_train, X_val, X_test
    )
    
    # Train model
    predictor.train_xgboost(X_train_scaled, y_train, X_val_scaled, y_val)
    
    # Evaluate
    metrics = predictor.evaluate_model(X_test_scaled, y_test)
    
    # Save model
    predictor.save_model()
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print("\n📦 Generated files:")
    print("   - ml-model/attrition_model.pkl (trained model)")
    print("   - ml-model/confusion_matrix.png")
    print("   - ml-model/roc_curve.png")
    print("   - ml-model/feature_importance.png")
    print("\n🚀 Ready for production deployment!")
    print("   Run: python ml-model/api.py")
    print("="*60 + "\n")
    
    # Test prediction
    print("\n🧪 Testing prediction with sample data...")
    sample = {
        'salary_growth': 5.0,
        'performance_score': 3.5,
        'promotion_gap': 4,
        'satisfaction_score': 6.0,
        'work_hours': 50,
        'overtime_frequency': 20
    }
    
    result = predictor.predict(sample)
    print(f"\nSample Input: {sample}")
    print(f"Prediction: {'ATTRITION RISK' if result['attrition'] else 'RETAINED'}")
    print(f"Attrition Probability: {result['attrition_probability']:.2%}")
    print(f"Retention Probability: {result['retention_probability']:.2%}")


if __name__ == "__main__":
    main()
