"""MERN stack component templates"""

PACKAGE_JSON_TEMPLATE = {
    "name": "${project_name}",
    "version": "1.0.0",
    "private": true,
    "scripts": {
        "dev": "vite",
        "build": "tsc && vite build",
        "preview": "vite preview",
        "lint": "eslint src --ext ts,tsx",
        "test": "vitest"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-router-dom": "^6.15.0",
        "zustand": "^4.4.1",
        "axios": "^1.5.0",
        "@tanstack/react-query": "^4.33.0",
        "tailwindcss": "^3.3.3",
        "postcss": "^8.4.28",
        "autoprefixer": "^10.4.15"
    },
    "devDependencies": {
        "@types/react": "^18.2.21",
        "@types/react-dom": "^18.2.7",
        "@typescript-eslint/eslint-plugin": "^6.6.0",
        "@typescript-eslint/parser": "^6.6.0",
        "@vitejs/plugin-react": "^4.0.4",
        "eslint": "^8.48.0",
        "typescript": "^5.2.2",
        "vite": "^4.4.9",
        "vitest": "^0.34.3"
    }
}

BACKEND_PACKAGE_JSON_TEMPLATE = {
    "name": "${project_name}-backend",
    "version": "1.0.0",
    "private": true,
    "scripts": {
        "start": "node dist/server.js",
        "dev": "nodemon src/server.ts",
        "build": "tsc",
        "test": "jest"
    },
    "dependencies": {
        "express": "^4.18.2",
        "mongoose": "^7.5.0",
        "cors": "^2.8.5",
        "dotenv": "^16.3.1",
        "express-validator": "^7.0.1",
        "jsonwebtoken": "^9.0.2",
        "bcryptjs": "^2.4.3",
        "winston": "^3.10.0"
    },
    "devDependencies": {
        "@types/express": "^4.17.17",
        "@types/node": "^20.5.7",
        "@types/cors": "^2.8.13",
        "@types/jest": "^29.5.4",
        "typescript": "^5.2.2",
        "nodemon": "^3.0.1",
        "ts-node": "^10.9.1",
        "jest": "^29.6.4",
        "ts-jest": "^29.1.1"
    }
}

TSCONFIG_TEMPLATE = {
    "compilerOptions": {
        "target": "ES2020",
        "useDefineForClassFields": True,
        "lib": ["ES2020", "DOM", "DOM.Iterable"],
        "module": "ESNext",
        "skipLibCheck": True,
        "moduleResolution": "bundler",
        "allowImportingTsExtensions": True,
        "resolveJsonModule": True,
        "isolatedModules": True,
        "noEmit": True,
        "jsx": "react-jsx",
        "strict": True,
        "noUnusedLocals": True,
        "noUnusedParameters": True,
        "noFallthroughCasesInSwitch": True
    },
    "include": ["src"],
    "references": [{ "path": "./tsconfig.node.json" }]
}
